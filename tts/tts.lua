--[[ Lua code. See documentation: https://api.tabletopsimulator.com/ --]]

--[[ The onLoad event is called after the game save finishes loading. --]]
function onLoad()
    broadcastToAll("use \"!generate\" to generate all the cards anew", {1,1,1})
    --[[ print('onLoad!') --]]
end

--[[ The onUpdate event is called once per frame. --]]
function onUpdate()
    --[[ print('onUpdate loop!') --]]
end

function onChat(message, player)
    if message == "!generate" then
        generateAllDecks()
        return false
    end
    return true
end

function generateAllDecks()
    broadcastToAll("Generating all decks...", {1,1,1})
end