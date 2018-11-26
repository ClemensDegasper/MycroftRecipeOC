from SPARQLWrapper import SPARQLWrapper, JSON
import pprint
totalTriple = 538168

def getRecipeByIngredient(ingredients):
	sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
	
	whereQuery = ""
	i = 0
	for ingre in ingredients:
		whereQuery += """?s schema:recipeIngredient ?ingredient%s .
			FILTER regex(?ingredient%s, "%s", "i")""" % (i,i,ingre)
		i += 1
		
	print(whereQuery)
	query = """
		PREFIX schema: <http://schema.org/>
		PREFIX ent: <http://www.ontotext.com/owlim/entity#>
		SELECT  ?name ?id ?description ?totalTime ?cookTime ?prepTime ?yield
		FROM <https://broker.semantify.it/graph/O7PY8ri5T2/WxGcA2Nj1O/latest>
		WHERE {
			?s a schema:Recipe .
			?s schema:name ?name .
			?s ent:id ?id .
			?s schema:description ?description .
			?s schema:totalTime ?totalTime .
			?s schema:cookTime ?cookTime .
			?s schema:prepTime ?prepTime .
			?s schema:recipeYield ?yield .
			%s
		} ORDER BY RAND()
		LIMIT 5
	""" % (whereQuery)
	
	print(query)
	
	sparql.setReturnFormat(JSON)
 
	sparql.setQuery(query)
	
	return sparql.query().convert()


def getRecipeIngredientsById(ID):
	sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph") 
	query = """
		PREFIX schema: <http://schema.org/>
		PREFIX ent: <http://www.ontotext.com/owlim/entity#>
		SELECT  ?ingredient
		FROM <https://broker.semantify.it/graph/O7PY8ri5T2/WxGcA2Nj1O/latest>
		WHERE {
			?s a schema:Recipe .
			?s ent:id "%s".
			?s schema:recipeIngredient ?ingredient
		}
	""" % (ID)
	
	sparql.setReturnFormat(JSON)
	print(query)
 
	sparql.setQuery(query)
	
	return sparql.query().convert()
	

def getInstructionsById(ID):
	sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph") 
	
	query = """
		PREFIX schema: <http://schema.org/>
		PREFIX ent: <http://www.ontotext.com/owlim/entity#>
		SELECT  ?pos ?text
		FROM <https://broker.semantify.it/graph/O7PY8ri5T2/WxGcA2Nj1O/latest>
		WHERE {
			?s a schema:Recipe .
			?s ent:id "%s".
			?s schema:recipeInstructions ?instructions .
			?instructions schema:text ?text.
			?instructions schema:position ?pos
		}
	""" % (ID)
	
	print(query)
	
	sparql.setReturnFormat(JSON)
 
	sparql.setQuery(query)
	
	return sparql.query().convert()
		
#print(getRecipeByIngredient(["Tomato","chicken"]))
#print(getRecipeIngredientsById("10532702"))
#getInstructionsById("10532702")

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(getRecipeByIngredient(["Tomato"]))#["results"]["bindings"][0]["description"]["value"])
pp.pprint(getInstructionsById(10663398))

