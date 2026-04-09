#  Secure Decentralized Federated Learning using Gossip Protocol

##  Overview

This project implements a **fully decentralized federated learning (FL) system** using a **gossip-based communication protocol** and **post-quantum cryptographic signatures (Dilithium)** for secure model updates.

Unlike traditional federated learning systems that rely on a **central server**, this implementation eliminates central aggregation and enables **peer-to-peer model exchange and aggregation**.

---

##  Key Features

-  **Decentralized Training**  
  No central server is used for aggregation — all nodes collaborate via peer-to-peer gossip.

-  **Gossip Protocol Communication**  
  Model updates are propagated using a **push-based randomized gossip protocol**.

-  **Post-Quantum Security (Dilithium)**  
  Each client signs its model updates using **Dilithium digital signatures**, ensuring integrity and authenticity.

-  **Local Model Aggregation**  
  Each node aggregates received updates independently (decentralized FedAvg-style).

-  **Efficient Propagation**  
  Controlled using:
  - `fanout` (number of peers)
  - `max_hops` (propagation depth)

---

##  System Architecture
