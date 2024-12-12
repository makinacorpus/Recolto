[![Coding standards](https://github.com/makinacorpus/db-tools-bundle/actions/workflows/coding-standards.yml/badge.svg)](https://github.com/makinacorpus/db-tools-bundle/actions/workflows/coding-standards.yml) [![Static Analysis](https://github.com/makinacorpus/db-tools-bundle/actions/workflows/static-analysis.yml/badge.svg)](https://github.com/makinacorpus/db-tools-bundle/actions/workflows/static-analysis.yml) [![Documentation build](https://github.com/makinacorpus/DbToolsBundle/actions/workflows/docs-build.yml/badge.svg)](https://github.com/makinacorpus/DbToolsBundle/actions/workflows/docs-build.yml) [![Continuous Integration](https://github.com/makinacorpus/DbToolsBundle/actions/workflows/continuous-integration.yml/badge.svg)](https://github.com/makinacorpus/DbToolsBundle/actions/workflows/continuous-integration.yml)

![RecoltO](/public/assets/logo_recolto_violet.png)

[![GitHub stars](https://img.shields.io/github/stars/makinacorpus/RecoltO)](https://github.com/makinacorpus/RecoltO/stargazers)

# Welcome to Récolt'Ô

The official Récolt'Ô repository for the 2024 Open Booster.

👉🏻 [Try Récolt'Ô](https://recolto.netlify.app/)

In March 2023, water tables remain below normal, with 80% of levels between low and very low. Faced with the problems caused by our personal uses, how can we avoid using drinking water when rainwater would be perfectly suitable? What savings could I make by installing a water recovery system? With the global warning, will my installation still be suitable in 2, 5 or 10 years' time?

Récolt'Ô is designed to support the deployment of water recovery systems on all types of buildings. There's a wide range of products on the market, but how do you choose the right size of tank? And to which roof pitch should it be connected? Récolt'Ô will help you determine the right tank volume based on local rainfall forecasts and individual water usage, while providing an unbiased estimate of expected savings.

![image](https://makina-corpus.com/sites/default/files/styles/600x500/public/2023-11/image.png.webp?itok=W9s7EmsA)

The benefits of this solution are manifold:
* **Optimization of water consumption**: By using rainwater for non-potable needs such as watering gardens, washing tools, or even toilets, users can reduce their dependence on drinking water, helping to preserve this precious resource.
* **Adaptability to changing weather conditions**: Thanks to climate and usage simulations, Récolt'Ô can determine the right tank volume for each situation, guaranteeing efficient, sustainable use of rainwater, even in a changing climate.
* **Reduced pressure on drinking water networks**: By encouraging the use of rainwater for non-drinking needs, Récolt'Ô helps to relieve the pressure on drinking water networks, reducing the risk of shortages and over-consumption.

By combining technological expertise, predictive analysis and a commitment to ecological resilience, Récolt'Ô represents an innovative and effective solution to the growing challenges of water management. By adopting Récolt'Ô, private individuals and professionals can not only contribute to preserving the environment, but also make significant savings on their drinking water consumption, while ensuring responsible use of natural resources.


## Data Story and Architecture

![Architecture diagram](project_architecture.png)

Récolt'Ô integrates multiple datasets to deliver precise water management insights:

- **calculating roof surface area**
Using the [BAN API](https://www.data.gouv.fr/fr/dataservices/api-adresse-base-adresse-nationale-ban/) we convert addresses into precise latitude and longitude coordinates, enabling us to center satellite imagery on the desired building and accurately measure its roof area.
- **estimating daily rainfall for specific locations:**
Currently, we leverage Copernicus data for global rainfall estimates. However, we are transitioning to the Météo France API to enhance the accuracy of rainfall data, providing more reliable insights tailored to specific locales.
- **estimating monthly water usage:**
Water consumption calculations are based on national statistics provided by the Water Information Center, ensuring an accurate reflection of typical usage patterns.
- **calculate water pricing:**
By referencing data from the [National Observatory of Water and Sanitation Utilities](https://www.services.eaufrance.fr/), we estimate water tariffs in France. This allows us to calculate potential financial savings from implementing water recovery systems

## Installation

**Installing dependencies**

```bash
nvm use
npm ci
```

### Development server

Starts the dev server at `http://localhost:3000`:

```bash
npm run dev
```

### Production build

Builds the application for production deployment:

```bash
npm run build
```

You can preview the build locally:

```bash
npm run preview
```

## Contributing

You want to help to build and improve the DbToolsBundle? Here is want you can do:
- Talk about it: share this project to make it more visible
- Report bugs you find: [Reporting issues](https://github.com/makinacorpus/Recolto/issues) is essential to help us improve this tool. Feel confident enough to correct it? PRs are welcome!
- Want to add missing functionnality? Create an [issue](https://github.com/makinacorpus/Recolto/issues)!
- Want to start developing ? Look at ["good first issues"](https://github.com/makinacorpus/recolto/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22)

## Looking Forward

Here's a summary of how Récolt'Ô can be extended to provide an even better experience for the community:
- Using climate projection data. By going further and exploring the use of data from different climate change scenarios, we hope to raise awareness among service users of the challenges of saving on their water consumption and encourage changes in behavior.
- Expand information on the uses that rainwater could cover. Enable users to record their simulated water consumption to derive more precise estimates of how much water the user needs to collect.
- Automatically detect the roof of one or more buildings based on an address.
- Take into account the footprint required to install a water collector and validate the feasibility of such an installation.
- Monitor changes in consumption after the addition of this device to their home, and compare with the average consumption of equivalent households in the same area.


## Licence

This software is published under the [MIT License](./LICENCE.md).

