WIKIDATA_REQUEST1 = """SELECT DISTINCT ?item ?itemLabel ?scientific_name ?taxinomic_rank ?taxinomic_rankLabel ?upper_taxon ?upper_taxonLabel ?citesid ?image ?value ?valueLabel
WHERE
{
  ?item wdt:P2040 ?value;
        rdfs:label ?itemLabel .
  OPTIONAL { ?item wdt:P18 ?image. }   
  OPTIONAL { ?item wdt:P225 ?scientific_name. } 
  OPTIONAL { ?item wdt:P105 ?taxinomic_rank. 
             ?taxinomic_rank rdfs:label ?taxinomic_rankLabel filter (lang(?taxinomic_rankLabel) = "en") .  
           }   
  OPTIONAL { ?item wdt:P171 ?upper_taxon. 
             ?upper_taxon rdfs:label ?upper_taxonLabel filter (lang(?upper_taxonLabel) = "en") .  
           }            
  OPTIONAL { ?item wdt:P2040 ?citesid. } 

  FILTER (LANG(?itemLabel)="en") }"""