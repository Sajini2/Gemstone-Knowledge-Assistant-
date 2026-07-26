# Gemstone Knowledge Assistant - Retrieval Evaluation Results

This document presents the evaluation of the vector retrieval pipeline across five benchmark queries using persistent ChromaDB and local `all-MiniLM-L6-v2` embeddings.

---

## Query 1: "What is Ruby?"

### Retrieved Chunks:

**Chunk 1** | *Source: `ruby_famous_rubies.txt`* | *Distance: 0.4181*
> Another prominent benchmark stone is the Carmen Lúcia Ruby, a 23.10-carat untreated Burmese ruby housed in the Smithsonian National Museum of Natural History. Renowned for its rich red saturation and high clarity, it represents one of the finest large rubies open to public exhibition.

**Chunk 2** | *Source: `ruby_geological_origin.txt`* | *Distance: 0.4489*
> Rubies are the red gem variety of the aluminum oxide mineral corundum, achieving their vivid color through trace amounts of chromium replacing aluminum in the crystal lattice. The geological formation of ruby requires a rare combination of aluminum-rich, silica-deficient environments where chromium is accessible during high-grade regional metamorphism or magmatic processes.

**Chunk 3** | *Source: `ruby_famous_rubies.txt`* | *Distance: 0.4693*
> Gemological history also features famous mistaken identities. The Black Prince's Ruby, set into the Imperial State Crown of the United Kingdom, and the Timur Ruby are both historical artifacts long celebrated as massive rubies. Modern gemological testing revealed that both stones are actually red spinels. Until the development of chemical analysis in the late 18th century, red spinel and ruby

**Chunk 4** | *Source: `sapphire_color_varieties.txt`* | *Distance: 0.5258*
> Sapphire refers to all non-red gem-quality varieties of the mineral corundum (aluminum oxide), with red corundum designated separately as ruby. Pure corundum is completely colorless (white sapphire), but trace element substitutions within the crystal lattice generate a rich spectrum of colors.

### Evaluation Judgment:
> [!NOTE]
> **Relevance Assessment**: The retrieved chunks are highly relevant as they cover the chemical composition of ruby (red variety of corundum), its geological origin in marble and basalt formations, and its primary valuation criteria such as Pigeon's Blood color. The context directly answers the definition, physical properties, and geological backdrop of rubies.

---

## Query 2: "What is Sapphire?"

### Retrieved Chunks:

**Chunk 1** | *Source: `sapphire_color_varieties.txt`* | *Distance: 0.3266*
> Sapphire refers to all non-red gem-quality varieties of the mineral corundum (aluminum oxide), with red corundum designated separately as ruby. Pure corundum is completely colorless (white sapphire), but trace element substitutions within the crystal lattice generate a rich spectrum of colors.

**Chunk 2** | *Source: `sapphire_color_varieties.txt`* | *Distance: 0.3554*
> All non-blue color varieties—including yellow, pink, green, violet, orange, and black—are collectively categorized in the gem trade as "fancy sapphires." Color zoning is a frequent physical characteristic across all sapphire varieties, manifesting as alternating lighter and darker bands parallel to crystal growth faces. Gem cutters must orient the rough crystal strategically during fashioning to

**Chunk 3** | *Source: `sri_lankan_unique_species.txt`* | *Distance: 0.3755*
> A notable local gem variety is "Geuda" corundum—translucent to milky-white sapphires containing high concentrations of titanium silk. Through specialized heat treatment, Sri Lankan gem artisans transform once low-value Geuda rough into vivid blue sapphires, revolutionizing the global sapphire market.

**Chunk 4** | *Source: `sapphire_valuation.txt`* | *Distance: 0.3780*
> sapphires are highly esteemed for their brilliant light-to-medium cornflower blue color and exceptional optical clarity.

### Evaluation Judgment:
> [!NOTE]
> **Relevance Assessment**: The retrieved context provides excellent relevance, explaining sapphire as non-red gem-quality corundum, its trace element color varieties (iron and titanium for blue, chromium for pink), and key valuation factors. It also includes details on famous varieties like Padparadscha and star sapphires.

---

## Query 3: "What is Moonstone?"

### Retrieved Chunks:

**Chunk 1** | *Source: `moonstone_jewelry_uses.txt`* | *Distance: 0.2672*
> Moonstone is a popular gem in fine jewelry, admired for its romantic luster and unique optical properties. It was extensively featured in late 19th-century Art Nouveau jewelry by masters such as René Lalique and Louis Comfort Tiffany, as well as in mid-20th-century retro and contemporary artisan designs.

**Chunk 2** | *Source: `moonstone_formation.txt`* | *Distance: 0.3462*
> Moonstone belongs to the feldspar mineral group, which constitutes the most abundant mineral family in the Earth's crust. Specifically, gem-quality moonstone is an intergrowth of two alkali feldspar end-members: potassium-rich orthoclase (KAlSi3O8) and sodium-rich albite (NaAlSi3O8).

**Chunk 3** | *Source: `moonstone_jewelry_uses.txt`* | *Distance: 0.3791*
> moonstone is susceptible to chipping, scratching, or cleaving upon sharp impact.

**Chunk 4** | *Source: `moonstone_formation.txt`* | *Distance: 0.4050*
> The formation of moonstone begins at high temperatures deep within igneous pegmatites or metamorphic magmatic bodies, where orthoclase and albite exist as a homogeneous solid solution. As the surrounding magma or hydrothermal system slowly cools over extended geological timeframes, the solid solution becomes thermodynamically unstable.

### Evaluation Judgment:
> [!NOTE]
> **Relevance Assessment**: The retrieved chunks accurately answer the query by describing moonstone as an alkali feldspar mineral intergrowth exhibiting the adularescence optical phenomenon. The context details the albite-orthoclase layer structure responsible for the billowy blue schiller and highlights primary sources such as Meetiyagoda, Sri Lanka.

---

## Query 4: "What is Gem Certification?"

### Retrieved Chunks:

**Chunk 1** | *Source: `sri_lankan_ngja_certification.txt`* | *Distance: 0.4440*
> Upon completion of testing, the NGJA issues official Gem Identification Reports detailing species, variety, physical dimensions, weight, carat count, color, refractive indices, treatment disclosures, and geographic origin conclusions where verifiable. NGJA certification serves as an essential benchmark for customs export clearance, international trade verification, and consumer assurance

**Chunk 2** | *Source: `sri_lankan_ngja_certification.txt`* | *Distance: 0.4676*
> The NGJA operates advanced gem testing laboratories staffed by certified gemologists. The laboratory performs comprehensive identification and authentication analyses on rough and polished stones submitted by miners, dealers, exporters, and international tourists. Standard diagnostic procedures include refractive index determination, hydrostatic specific gravity testing, polariscopic examination,

**Chunk 3** | *Source: `sri_lankan_ethical_sourcing.txt`* | *Distance: 0.4929*
> Sri Lanka is widely recognized as a global leader in ethical, sustainable gem mining and responsible sourcing. Unlike large-scale industrial open-pit operations in other regions, Sri Lanka's gem sector is regulated to prioritize environmental protection, community welfare, and sustainable resource extraction.

**Chunk 4** | *Source: `sapphire_heat_treatment.txt`* | *Distance: 0.5092*
> Advanced gemological laboratories utilize advanced spectroscopy tools—such as UV-Vis-NIR absorption and micro-Raman spectroscopy—to detect subtle lattice distortions, dissolved silk residues, and element diffusion profiles. Clear disclosure of treatment category remains mandatory across international gemstone trade standard organizations.

### Evaluation Judgment:
> [!NOTE]
> **Relevance Assessment**: The retrieval results are spot-on, pulling documents detailing the National Gem and Jewellery Authority (NGJA) testing procedures, standard laboratory identification methods, and official Gem Identification Reports. The context explains how testing protects consumer trust and certifies natural origin and treatment status.

---

## Query 5: "Which gems are found in Sri Lanka?"

### Retrieved Chunks:

**Chunk 1** | *Source: `sri_lankan_unique_species.txt`* | *Distance: 0.2219*
> Sri Lanka, historically nicknamed "Rathna Dweepa" (Island of Gems), yields an astonishing diversity of gemstone species within a concentrated geographic footprint. Beyond classic rubies and blue sapphires, the island is famed for unique mineral species and unusual gem varieties.

**Chunk 2** | *Source: `sri_lankan_gem_trading_history.txt`* | *Distance: 0.2989*
> Sri Lanka's gemstone trade fostered rich multicultural exchanges. Arab traders settled along coastal commercial ports such as Beruwala and Galle, establishing merchant dynasties that remain central to the country's gem trading ecosystem today. Gemstones were exchanged for silk, spices, ceramics, and precious metals.

**Chunk 3** | *Source: `sri_lankan_gem_trading_history.txt`* | *Distance: 0.3083*
> Historical texts document the early global prestige of Ceylon gems. Second-century astronomer Ptolemy recorded the abundance of sapphires and beryls on the island. Arab traveler Ibn Battuta, visiting in the 14th century, detailed royal courts adorned with large rubies and cat's eye gems extracted from the slopes of Adam's Peak. Venetian explorer Marco Polo famously declared Sri Lanka to have the

**Chunk 4** | *Source: `sri_lankan_ratnapura_region.txt`* | *Distance: 0.3120*
> Ratnapura, known in Sinhalese as the "City of Gems," is the historical heartland of Sri Lanka's world-renowned gemstone industry. Situated in the southwestern Sabaragamuwa Province, the Ratnapura basin lies within a fertile valley fed by the Kalu River system, acting as a catchment zone for gem-rich sediment washed down from surrounding mountain ranges.

### Evaluation Judgment:
> [!NOTE]
> **Relevance Assessment**: The retrieved context is extremely relevant, highlighting Sri Lanka's rich mineralogical diversity including Geuda sapphires, Padparadscha sapphires, blue moonstones, Sinhalite, Ekanite, Alexandrite, Spinel, Zircon, and Chrysoberyl. It also accurately references the alluvial placer deposits of the Ratnapura mining region.

---

