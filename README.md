# RIG
Rig - Random Iterated Greedy, progetto per Algoritmi di Ottimizzazione

Nelle seguenti righe vedremo un estratto della relazione, per maggiori informazioni, come nomenclatura e equazioni, rimando alla documentazione completa.

  # Introduzione
  Il problema in oggetto è un problema di scheduling di jobs su macchine parallele identiche con l'obiettivo di minimizzare la total tardiness.
  Viene proposta una dispatching rule e valutata comparandola con altri approcci esistenti.
  Inoltre, è sviluppato un metodo metaeuristico greedy-based per migliorare la soluzione iniziale.
  I risultati mostrano che la metaeuristica proposta performa meglio degli approcci comparati in questo elaborato.
   Il problema affrontato consiste in n jobs processati su m macchine parallele identiche.
  Ogni job J_i ha uno specifico processing time p_i e un due date d_i, e può essere processato arbitrariamente su qualunque macchina.
  Potrebbe intercorrere un setup time tra due job consecutivi sulla stessa macchina, se essi hanno valori diversi per qualche A_a.
  Tutte le macchine sono pronte al tempo 0, come anche i jobs.
  Non sono ammesse interruzioni e preemption, e non ci sono priorità.
  Una macchina può processare al massimo un job alla volta, ed il job può essere processato da una sola macchina.
  L'obiettivo è trovare uno schedule che minimizzi la tardiness totale.
  La tardiness è definita come T_i = max{C_i-d_i, 0}.
  La funzione oggetto è di minimizzare la sommatoria delle T_i, per ogni job, per ogni macchina.
    
  # Metodo di scheduling 0
  Il primo metodo di scheduling che vediamo è quello di utilizzare le regole LPT e EDD.
      La regola LPT (Longest Processing Time first) consiste nell'ordinare i jobs in ordine decrescente per il processing time ed assegnarli alle macchine via via che si liberano, in modo da migliorare il bilanciamento del carico.
      La regola EDD (Earliest Due Date first) consiste nell'ordinare i jobs in ordine crescente per il due date, in modo da evitare il più possibile che essi finiscano in ritardo.
      L'algoritmo qui utilizzato si divide in due fasi:
          Step 1. Scegli il job J_i con il processing time più lungo ed assegnalo alla prima macchina disponibile. Ripeti fino a che tutti i jobs sono assegnati.
          Step 2. Per ogni macchina, riordina i jobs in ordine crescente per la due date.
    
  # Metodo di scheduling 1 - ATCS
  Il secondo metodo implementato è stato preso in prestito dalla regola data da Lee e Pinedo.
  L' Apparent Tardiness Cost with Setups (ATCS) index è una regola molto usata nei problemi di scheduling per minimizzare la total tardiness.
  L'idea di base è quella di calcolare l'ATCS per ogni job non processato e pronto quando una macchina diventa libera.
  Successivamente, il job con l'ATCS più alto viene scelto ed assegnato sulla macchina libera.
  L'ATCS prende in considerazione i processing time, i minimum slack ed i setup-time in un singolo ranking.
    
  #Metodo di scheduling 2 - ATCS + APD
  Introduciamo prima l'index APD (Adjacent Processing Time) utilizzato per sviluppare questa euristica.
  L'indice APD prende in considerazione il processing time, il due date ed i setuptimes. In riferimento a questi ultimi, vengono considerati anche quanti valori di questi sono comuni tra i job (flessibilità).
  
  Definito l'APD index, si andrà ora ad integrare con l'ATCS formando l'ATCS_APD, che prenderà in considerazione entrambi gli indici per una maggior precisione.
  
  Il job con ATCS_APD maggiore è considerato quello con priorità maggiore.
  Di seguito vengono mostrati i passi per implementare il metodo ATCS_APD:
      Step 1. Per ogni job i calcola l'APD_i e setta t=0. 
      Step 2. Scegli la macchina k che è disponibile al tempo t e calcola I_ATCS_APD_i(t,j) per ogni job i non schedulato.
      Step 3. Il job i con I_ATCS_APD_i(t,j) maggiore è assegnato alla macchina k e viene settato il tempo t come il loading time della macchina k. Se ci sono ancora jobs non schedulati, allora torna a Step 2., altrimenti fermati.    
    
  #Metodo di scheduling 3 - ATCS_APD + RIG
  Infine, in questa sezione viene mostrato il Random Iterated Greedy (RIG).
  Questa metaeuristica tenta di migliorare le soluzioni fornite da ATCS_APD, seguendo un approccio greedy-based.
  L'approccio Iterated Greedy genera le soluzioni usando due fasi principali: distruzione e costruzione.
  Nella fase di distruzione, alcuni jobs vengono rimossi dalla soluzione corrente.
  Nella fase di costruzione, vengono applicate delle regole per riottenere una soluzione completa.
  Una volta ottenuta, viene usato un criterio per determinare se il nuovo scheduling viene accettato aggiornando il corrente. La procedura viene ripetuta fino a che non si raggiunge un criterio di stop.
  Questo studio propone un random iterated greedy per migliorare le soluzioni fornite da ATCS_APD.
  RIG itera tra 3 diversi stages: distruzione, costruzione e movement.
  L'idea è di avere diversi tipi di distruzione e di costruzione tra cui scegliere casualmente ad ogni iterazione, cosi da poter avere più alte chances di trovare soluzioni migliori.
  In particolare, si hanno 2 tipi di distruzione (DST_i) e 3 tipi di costruzione (CST_j, definiti come:
  Distruzione:
      Distruzione 1 (DST_1): Sceglie casualmente un job dalla macchina con la massima C_max
      Distruzione 2 (DST_2): Sceglie casualmente un job tra tutte le macchine
  Costruzione:
    Costruzione 1 (CST_1): Inserisce il job scelto tra tutte le possibili posizioni della macchina dalla quale viene
    Costruzione 2 (CST_2): Inserisce il job scelto tra tutte le possibili posizioni della macchina dalla quale viene e della macchina col minor C_max
    Costruzione 3 (CST_3): Inserisce il job scelto tra tutte le possibili posizioni di tutte le macchine
  
  I passi del RIG sono i seguenti:
  Ripetere i seguenti step fino a che non si raggiunge il numero massimo di iterazioni l=l_max:
    Step 0. Inizializzazione: solo alla prima iterazione, prendere soluzione iniziale X la soluzione ottenuta da ATCS_APD.
            Per l>1, selezionare casualmente due jobs dalla soluzione e scambiarli in modo da trovare una nuova soluzione X.
    Step 1. Distruzione: Selezionare a caso un DST_i e usarlo su X
    Step 2. Costruzione: Selezionare a caso un CST_j per costruire una nuova soluzione X'
    Step 3. Movement: Se X' è migliore di X, allora X prende X' e torna a Step 1., altrimenti, setta l=l+1 e torna a Step 0.
    
  Quindi, ricapitolando, si settano le condizioni iniziali nello step 0. Dopodiché, viene scelta casualmente una combinazione di DST_i e CST_j per generare una nuova soluzione. All'ultimo step, viene definita la condizione di fine.
