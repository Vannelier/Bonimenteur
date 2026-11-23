/* Hors de claude.ai : la base partagée des artifacts (window.claude) remplacée par
   l'API du serveur (app/main.py). Même interface que celle dont la page se sert :
   collection(nom).onSnapshot / .limit / .add, doc(chemin).set, user.id, user.profiles.
   Lecture : /api/etat au chargement, toutes les 20 s et après chaque écriture.
   Sur claude.ai, window.claude existe déjà et ce fichier ne fait rien. */
(() => {
  if (window.claude && window.claude.use) return;
  const RAFRAICHIR_MS = 20000;
  const abonnes = {};            // nom de collection -> fonctions
  let etat = null, enCours = null, moi = null;

  const docs = nom => {
    if (!etat) return [];
    if (nom === "mots") return Object.entries(etat.mots).map(([id, d]) => ({ id, d }));
    if (nom === "pieges") return etat.pieges.map(p => ({ id: p.id, d: p }));
    if (nom === "choix") return etat.choix.map(c => ({ id: c.id, d: c }));
    if (nom === "contestations") return etat.contestations.map(c => ({ id: `${c.piege}__${c.joueur}`, d: c }));
    if (nom === "joueurs") return Object.entries(etat.joueurs).map(([id, pseudo]) => ({ id, d: { pseudo } }));
    return [];
  };
  const instantane = nom => ({ docs: docs(nom).map(x => ({ id: x.id, data: () => x.d })), metadata: { fromCache: false } });
  const diffuser = () => { for (const [nom, fs] of Object.entries(abonnes)) for (const f of fs) f(instantane(nom)); };

  async function lire() {
    if (enCours) return enCours;
    enCours = fetch("/api/etat", { credentials: "same-origin" })
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(d => { etat = d; diffuser(); })
      .finally(() => { enCours = null; });
    return enCours;
  }
  async function ecrire(methode, url, corps) {
    const r = await fetch(url, { method: methode, credentials: "same-origin", headers: { "Content-Type": "application/json" }, body: JSON.stringify(corps) });
    if (!r.ok) { const e = new Error(`HTTP ${r.status}`); e.code = r.status === 402 ? "solde" : r.status === 409 ? "doublon" : String(r.status); throw e; }
    const reponse = await r.json();
    // La page relit l'état juste après : il doit être à jour. Une lecture partie avant
    // l'écriture ne compte pas, on en relance une.
    if (enCours) await enCours.catch(() => {});
    await lire().catch(() => {});
    return reponse;
  }
  const ROUTES = {
    pieges: d => ecrire("POST", "/api/pieges", { mot: d.mot, texte: d.texte, prix: d.prix || 10 }),
    choix: d => ecrire("POST", "/api/choix", { mot: d.mot, montres: d.montres || [], ordre: d.ordre || [], erreur: !!d.erreur }),
    signalements: d => ecrire("POST", "/api/signalements", { mot: d.mot, raison: d.raison, pieges: d.pieges || [] }),
  };
  const collection = nom => ({
    limit() { return this; },
    onSnapshot(f, erreur) {
      (abonnes[nom] = abonnes[nom] || []).push(f);
      if (etat) setTimeout(() => f(instantane(nom)), 0); else lire().catch(e => erreur && erreur(e));
      return () => { abonnes[nom] = abonnes[nom].filter(g => g !== f); };
    },
    async add(d) { if (!ROUTES[nom]) throw new Error(`collection ${nom} en lecture seule`); return ROUTES[nom](d); },
  });
  const doc = chemin => ({
    async set(d) {
      const [nom] = chemin.split("/");
      if (nom === "contestations") return ecrire("POST", "/api/contestations", { piege: d.piege, mot: d.mot });
      if (nom === "joueurs") return ecrire("PUT", "/api/pseudo", { pseudo: d.pseudo });
      throw new Error(`document ${chemin} en lecture seule`);
    },
  });
  const user = {
    async id() {
      if (!moi) moi = (await fetch("/api/moi", { credentials: "same-origin" }).then(r => r.json())).id;
      return moi;
    },
    async profiles(ids) {
      if (!etat) await lire();
      return Object.fromEntries(ids.filter(i => etat.joueurs[i]).map(i => [i, { name: etat.joueurs[i] }]));
    },
  };
  setInterval(() => { if (!document.hidden) lire().catch(() => {}); }, RAFRAICHIR_MS);
  window.claude = { use: async nom => nom === "db" ? { collection, doc } : nom === "user" ? user : null };
})();
