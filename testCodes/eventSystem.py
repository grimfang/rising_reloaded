





################## DELETE ##########################

# Could use callback like they did in torque3d also make use of the p3d messenger.

# So the player has method that pops and event on a collision.
# Player runs and collides with and itemObject with a bSensor, the playerOnCollision method 
# takes the item name it collided with and sends off an event with a name eventlistener, only one name
# for the events but the vars attached carry the eventname to be executed.

# We could also make use of bitmasks as the collisionEventname. for instance
# 0x4 = pickableObject like ammo
# 0x5 = pickableObject like Health bottle
# 0x6 = Switch on/off
# 0x7 = EdgeGrab
# 0x8 = wallRunZone or something..

"""
itemObject:
    model: "someModel"
    sensor: bulletSensor_Sphere
    bitmask: 0x4

"""

# playerObject:

# The PlayerPhysics will have a loop i guess for the events
contactType = {
    "pickup" : _player.messenger.send(*args) 
}

result = world.contactTest(_player)

for contact in result.getNumContacts():

    if contact in contactType.keys():

        collisionNode = contact.getNode1()
        contactType[contact](*args or collsisionNode)
        

"""
    model: "playerModel"
    sensor: "CheckFor new Collisions" or react on collision or w/e
    def onCollision(player):
        _collisionObject = getCollisionObject()
        _collisionType = getCollisionType() # a pickable object 

        _player.send("eventListener", (_collisionType, _collisionObject, _player))
"""


class EventHandler (DirectObject):

    def __init__(self, _engine):

        # Start the EventHandler
        self.accept("onCollision", self.onCollision(*args))

        self.events = {

            "pickup"    : Event.item_pickup(_itemname, _extras) # Vars from the directObject.messenger.send(_thisItem)
        }

    def onCollision(self, *args=EventName, node):

        
        _engine.GameObjects['player'].EventName(node)



# Different kinds of events
class Event():

    @classmethod
    def item_pickup(cls, _engine, _itemName, _extras):

        print "Pickup Item! %s " % (_itemName) # getItem that popped event

        # in player we have something like
        # playerBag = []

        # Here we take the item
        GameObjects['player'].playerbag.append(_itemName)
        #thatItemname. removeVisual from world






#############################################################################################3

# Way 2

###

# When a collision took place inside the PLayerPhysics module

result = world.contactTest(_player)

for contact in result.getNumContacts():

    node = contact.getNode1()
    eventType = nodeInstance.getEventType() 
    #we will have to setup items so that we can use the name to search for the instance
    _player.messenger.send("onCollision", [eventType, node])












