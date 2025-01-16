---
title: 'Sources de données'
order: 20
---

# Sources de données

Récolt'Ô intègre plusieurs ensembles de données pour fournir des informations précises sur la gestion de l'eau :

- **calcul de la surface des toits**
En utilisant l'[API BAN](https://www.data.gouv.fr/fr/dataservices/api-adresse-base-adresse-nationale-ban/), nous convertissons les adresses en coordonnées précises de latitude et de longitude, ce qui nous permet de centrer l'imagerie satellite sur le bâtiment souhaité et de mesurer avec précision la surface de son toit.
- **estimation des précipitations quotidiennes pour des lieux spécifiques :**
Actuellement, nous utilisons les données de Copernicus pour estimer les précipitations globales. Cependant, nous sommes en train de passer à l'API de Météo France afin d'améliorer la précision des données pluviométriques et de fournir des informations plus fiables adaptées à des lieux spécifiques.
- **estimation de la consommation d'eau mensuelle :**
Les calculs de consommation d'eau sont basés sur les statistiques nationales fournies par le [Centre d'information sur l'eau](https://www.cieau.com/), garantissant un reflet précis des habitudes de consommation.
- **calculer le prix de l'eau :**
En se référant aux données de l'[Observatoire national des services d'eau et d'assainissement](https://www.services.eaufrance.fr/), nous estimons les tarifs de l'eau en France. Cela nous permet de calculer les économies potentielles liées à la mise en place de systèmes de récupération de l'eau.

