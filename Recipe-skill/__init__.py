# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import RecipeSkill.SPARQLConnector as SparqlCon

class RecipeSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(RecipeSkill, self).__init__(name="RecipeSkill")
        

    @intent_handler(IntentBuilder("").require("search.recipe.with").require("Ingredients").build())
    def handle_hello_world_intent(self, message):
        ingredients = message.data.get("Ingredients")
        # todo make nice array from ingredients if multiple ingredients as input
        result = SparqlCon.getRecipeByIngredient([ingredients])["results"]["bindings"][0]
        name = result["name"]["value"]
        description = result["description"]["value"]
        self.speak_dialog("looking.for.recipe", data={"name": name, "description": description})


    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return RecipeSkill()
