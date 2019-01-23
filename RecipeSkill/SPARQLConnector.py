from SPARQLWrapper import SPARQLWrapper, JSON
import pprint as pp
totalTriple = 538168

def getRecipe(ingredients="", cuisine = "", categories = "", keywords=""):
	if ingredients == "" and cuisine == "" and categories == "" and keywords == "":
		print("error: no parameters were given")
		return;
	sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
	
	whereQuery = ""
	
	if ingredients != "":
		i = 0
		for ingre in ingredients:
			whereQuery += """?s schema:recipeIngredient ?ingredient%s .
				FILTER regex(?ingredient%s, "%s", "i")""" % (i,i,ingre)
			i += 1
	
	if cuisine != "":
		i = 0
	
		for cui in cuisine:
			whereQuery += """?s schema:recipeCuisine ?cui%s .
				FILTER regex(?cui%s, "%s", "i")""" % (i,i,cui)
			i += 1
	
	if categories != "":
		i = 0
	
		for cat in categories:
			whereQuery += """?s schema:recipeCategory ?cat%s .
				FILTER regex(?cat%s, "%s", "i")""" % (i,i,cat)
			i += 1
		
	if keywords != "":
		i = 0
		
		for key in keywords:
			whereQuery += """?s schema:keywords ?keyword%s .
				FILTER regex(?keyword%s, "%s", "i")""" % (i,i,key)
			i += 1
		
	
	
	print(whereQuery)
	query = """
		PREFIX schema: <http://schema.org/>
		PREFIX ent: <http://www.ontotext.com/owlim/entity#>
		SELECT distinct ?name ?id ?description ?totalTime ?cookTime ?prepTime ?yield ?keywords
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
			?s schema:keywords ?keywords .
			%s
		} ORDER BY RAND()
		
	""" % (whereQuery)
	
	print(query)
	
	sparql.setReturnFormat(JSON)
 
	sparql.setQuery(query)
	
	result = sparql.query().convert()
	
	orderedResult = []
	
	for r in result["results"]["bindings"]:
		res = 0
		for i in ingredients:
			#print(r)
			#print(i)
			res += evalIngredientInRecipe(i,r)
			#print(res)
		#print(res)
		#print(r["name"]["value"])
		orderedResult.append([r,res])
	
	#print(orderedResult)
	data = sorted(orderedResult,key=lambda x: x[1], reverse=True)
	
	data = [x[0] for x in data]
	print(data)

	return data

def evalIngredientInRecipe(ingre, jsonSet):
	name = jsonSet["name"]["value"]
	description = jsonSet["description"]["value"]
	keywords = jsonSet["keywords"]["value"]
	
	count = 0
	
	#print(name)
	#print(ingre)
	#print(keywords)
	
	
	count += name.lower().count(ingre.lower())
	count += description.lower().count(ingre.lower())
	count += keywords.lower().count(ingre.lower())

	
	return count


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
	
	return parseIngredientsToList(sparql.query().convert())
	
def parseIngredientsToList(unparsedIngredients):
    result = []
    for ingredient in unparsedIngredients["results"]["bindings"]:
        result.append(ingredient["ingredient"]["value"])
    return result
    
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
	
def getCategories():
	sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
	
	query = """
		PREFIX schema: <http://schema.org/>
		PREFIX ent: <http://www.ontotext.com/owlim/entity#>
		SELECT distinct ?cat
		FROM <https://broker.semantify.it/graph/O7PY8ri5T2/WxGcA2Nj1O/latest>
		WHERE {
			?s a schema:Recipe .
			?s schema:recipeCategory ?cat .
		}
	"""
	
	print(query)
	
	sparql.setReturnFormat(JSON)
 
	sparql.setQuery(query)
	
	return sparql.query().convert()	
	
def getCuisine():
	sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
	
	query = """
		PREFIX schema: <http://schema.org/>
		PREFIX ent: <http://www.ontotext.com/owlim/entity#>
		SELECT distinct ?cui
		FROM <https://broker.semantify.it/graph/O7PY8ri5T2/WxGcA2Nj1O/latest>
		WHERE {
			?s a schema:Recipe .
			?s schema:recipeCuisine ?cui .
		}
	"""
	
	print(query)
	
	sparql.setReturnFormat(JSON)
 
	sparql.setQuery(query)
	
	return sparql.query().convert()		
		
		

'''
def getRecipeByKeywords(keywords):
	sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
	
	whereQuery = ""
	i = 0
	for key in keywords:
		whereQuery += """?s schema:keywords ?keyword%s .
			FILTER regex(?keyword%s, "%s", "i")""" % (i,i,key)
		i += 1
		
	print(whereQuery)
	query = """
		PREFIX schema: <http://schema.org/>
		PREFIX ent: <http://www.ontotext.com/owlim/entity#>
		SELECT distinct ?name ?id ?description ?totalTime ?cookTime ?prepTime ?yield ?keywords
		FROM <https://broker.semantify.it/graph/O7PY8ri5T2/WxGcA2Nj1O/latest>
		WHERE {
			?s a schema:Recipe .
			?s schema:name ?name .
			?s ent:id ?id .
			?s schema:description ?description .
			?s schema:totalTime ?totalTime .
			?s schema:cookTime ?cookTime .
			?s schema:prepTime ?prepTime .
			?s schema:keywords ?keywords .
			?s schema:recipeYield ?yield .
			%s
		} ORDER BY RAND()
		LIMIT 5
	""" % (whereQuery)
	
	print(query)
	
	sparql.setReturnFormat(JSON)
 
	sparql.setQuery(query)
	
	return sparql.query().convert()
'''
'''
def getRecipeByCategory(categories):
	sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
	
	whereQuery = ""
	i = 0
	for cat in categories:
		whereQuery += """?s schema:recipeCategory ?cat%s .
			FILTER regex(?cat%s, "%s", "i")""" % (i,i,cat)
		i += 1
		
	print(whereQuery)
	query = """
		PREFIX schema: <http://schema.org/>
		PREFIX ent: <http://www.ontotext.com/owlim/entity#>
		SELECT distinct ?name ?id ?description ?totalTime ?cookTime ?prepTime ?yield
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
'''

'''
def getRecipeByCuisine(cuisine):
	sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
	
	whereQuery = ""
	i = 0
	for cui in cuisine:
		whereQuery += """?s schema:recipeCuisine ?cui%s .
			FILTER regex(?cui%s, "%s", "i")""" % (i,i,cui)
		i += 1
		
	print(whereQuery)
	query = """
		PREFIX schema: <http://schema.org/>
		PREFIX ent: <http://www.ontotext.com/owlim/entity#>
		SELECT distinct ?name ?id ?description ?totalTime ?cookTime ?prepTime ?yield
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
'''

		
		
#print(getRecipeByIngredient(["Tomato","chicken"]))
#print(getRecipeIngredientsById("10532702"))
#getInstructionsById("10532702")

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(getRecipeByIngredient(["Tomato","salt","sugar","olives"]))#["results"]["bindings"][0]["description"]["value"])
#pp.pprint(getInstructionsById(10663398))
#pp.pprint(getRecipeByCuisine(["german"]))#["results"]["bindings"][0]["description"]["value"])

#pp.pprint(getCuisine())
pp.pprint(getRecipeIngredientsById(getRecipe(cuisine=["italian"], keywords=["chicken"])[0]["id"]["value"]))
