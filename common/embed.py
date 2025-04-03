import os
import re

from collections import defaultdict, Counter
from logging import getLogger, basicConfig

# from nltk import download
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, semcor

# download("punkt"); download("punkt_tab"); download("stopwords"); download("semcor")

logger = getLogger(__name__)
basicConfig(level="INFO")

def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^ a-z]", "", text, count=99)
    return text

logger.info("Loading sentences.")
sentences = semcor.sents()

logger.info(f"Building corpus.")
# a chatgpt-generated list of nonsense sentences about the ship, plus one useful one.
corpus: list[str] = [
    "The Orion is 800 meters in length.",
    "The Orion's primary hull is made of reinforced titanium alloy.",
    "The ship's propulsion system is powered by a hybrid fusion-drive engine.",
    "The forward airlock is located on Deck 5.",
    "The Orion has 12 docking ports for external spacecraft.",
    "The spacecraft's fuel tanks are pressurized at 2.5 atmospheres.",
    "The cargo hold can accommodate up to 5,000 metric tons of supplies.",
    "The life support system is capable of sustaining 250 crew members for 3 years.",
    "The hull is designed to withstand radiation levels up to 500 millisieverts per day.",
    "The primary communication array is located on Deck 3.",
    "The ship's main computer is housed in a temperature-controlled environment on Deck 2.",
    "The Orion has 48 external cameras for navigation and security.",
    "The spaceship's outer hull is coated with a layer of heat-resistant ceramic.",
    "The main thrusters are located at the rear of the ship.",
    "The Orion is equipped with 4 auxiliary ion engines for maneuvering.",
    "The gravity generators are set to simulate 0.85G.",
    "There are 6 escape pods on the ship, each with a capacity of 8 crew members.",
    "The auxiliary power systems run on hydrogen fuel cells.",
    "The ship has a total of 45 emergency escape routes.",
    "The air filtration system can cycle the ship's air supply every 10 minutes.",
    "The primary medical bay is located on Deck 7.",
    "The Orion has a total of 10 laboratories.",
    "The ship's AI, Aurora, is stored in a secure, redundant data core.",
    "The Orion is equipped with an anti-gravity basketball court.",
    "The main observation deck is located on Deck 8 and offers a 360-degree view.",
    "The Orion has a built-in hydroponics garden for crew sustenance.",
    "The exterior lighting system uses LED lights, lasting up to 10,000 hours.",
    "The ship's reactor is located on Deck 10, at the core of the ship.",
    "The artificial gravity system is powered by the fusion engine's byproducts.",
    "The ship's hull is divided into 50 sectors for maintenance and repair purposes.",
    "There are 72 maintenance drones assigned to hull inspection tasks.",
    "The Orion has 200 kilometers of fiber-optic wiring throughout the ship.",
    "The ship's AI system, Aurora, is capable of running 200 different diagnostic programs simultaneously.",
    "The primary crew quarters are located on Deck 4.",
    "The Orion has a built-in 3D printing facility for manufacturing parts.",
    "The ship's emergency lighting system activates upon a hull breach.",
    "The Orion has a total of 8 waste disposal units.",
    "The external cargo bay doors are hydraulically operated.",
    "The main hallways are 3 meters wide to accommodate emergency vehicles.",
    "The ship's airlock can open in 8 seconds, with an automatic pressure equalization.",
    "There are 15 personal data terminals throughout the ship for crew communication.",
    "The Orion's fire suppression system uses inert gas instead of water.",
    "The ship's docking system uses magnetic locks for secure connections.",
    "The Orion has an automatic self-destruct system, which requires 3 independent authorizations to activate.",
    "The mainframe computer requires cooling from an external radiator to maintain optimal temperatures.",
    "The AI Aurora has a voice-modulation system that can mimic human tones.",
    "The ship's hull is segmented into 12 blast-proof zones.",
    "The Orion has a dedicated leisure area with a small pool.",
    "The ship's hull plating is 4 meters thick in high-stress areas.",
    "There is an onboard printing station on Deck 6 for crew documents.",
    "The Orion's energy shields can withstand impacts from micrometeoroids traveling up to 40,000 kilometers per hour.",
    "The ship's exterior has 18 retractable solar panels.",
    "The Orion's hull is resistant to micrometeoroid damage, capable of self-healing through nanite technology.",
    "The main observation windows are made from reinforced, transparent polycarbonate.",
    "The Orion has 3 separate oxygen recycling units.",
    "The ship's interior walls are lined with soundproof panels.",
    "The ship's cryo-chambers are equipped with automated thawing and diagnostic systems.",
    "The AI Aurora is responsible for maintaining the ship's communication links with external networks.",
    "The Orion's fire suppression system can detect smoke or heat in less than 2 seconds.",
    "The escape pods are equipped with emergency beacons to signal distress.",
    "The Orion's reactor produces 3.5 gigawatts of power at full capacity.",
    "The ship's central computer network uses quantum encryption for security.",
    "The Orion's bridge is located on Deck 2.",
    "The ship's power grid is divided into 8 separate segments to prevent total failure.",
    "The Orion is equipped with 4 ionized propulsion engines for deep-space travel.",
    "The ship's exterior is covered with heat-dissipating plates.",
    "The air supply on the ship is treated with a low-level ionization process.",
    "The Orion's bridge has an array of 24 interactive touchscreens for navigation.",
    "The spacecraft's cargo hold is secured by a magnetic containment field.",
    "The Orion has a zero-gravity recreation room on Deck 9.",
    "The ship's ion engines have a maximum thrust of 20,000 kilonewtons.",
    "The Orion's thermal regulation system ensures temperature consistency within 1°C.",
    "The onboard library contains 1,200,000 digital books.",
    "The Orion has 36 separate communication channels.",
    "The ship's primary radar array is capable of detecting objects up to 100,000 kilometers away.",
    "The ship's plumbing system uses water recycling from waste products.",
    "The ship's paint job uses a special reflective coating to reduce heat absorption.",
    "The Orion has a fleet of 4 small scout drones for planetary exploration.",
    "The cargo hold can be accessed through a pair of hydraulic doors.",
    "The Orion's optical sensors can distinguish objects with a resolution of up to 1 millimeter.",
    "The AI system's voice interface can recognize up to 100 different languages.",
    "The Orion's heat shield can withstand re-entry speeds of up to 12 kilometers per second.",
    "The spacecraft uses laser communications for deep-space signal transmission.",
    "The main kitchen area has 15 food synthesizers for crew meals.",
    "The AI Aurora can override manual controls in case of system failure.",
    "The Orion has a built-in music system in every crew room.",
    "The ship's hull is designed to withstand pressures up to 1,000 pascals.",
    "The Orion's escape pods use an automated guidance system to return to the nearest habitable planet.",
    "The ship's system diagnostics run every 4 hours automatically.",
    "The Orion has 14 full-size bathrooms for the crew.",
    "The ship's interior temperature can be adjusted in each individual room.",
    "The AI system, Aurora, can predict system failures based on historical data trends.",
    "The Orion uses a central cooling system to regulate all critical components.",
    "The spaceship has 2 large recreational halls for crew social events.",
    "The ship's airlocks can seal in under 5 seconds in the event of a hull breach.",
    "The Orion uses a hybrid system of kinetic and solar power for auxiliary functions.",
    "The ship's central elevator system operates on a magnetic levitation platform.",
    "The Orion is equipped with a self-repair system that uses nanobots for minor hull damage.",
    "The spaceship's onboard gym includes 6 treadmill units and 10 exercise stations.",
    "The Orion's cargo hold has automated systems for palletizing and moving heavy loads.",
    "The Orion's main reactor is designed with a master control override for emergency shutdowns.",
    "Aurora performs a system reset every 72 hours to maintain optimal functionality.",
    "The Orion's primary navigation system can be overridden by Aurora in case of manual failure.",
    "The ship's hull is equipped with a master encryption code to prevent unauthorized access.",
    "Aurora can reset any non-critical system to factory settings upon command.",
    "The Orion's central core can be overridden by Aurora for diagnostics.",
    "The master command console on Deck 2 contains an override function to disable the ship's AI temporarily.",
    "Aurora is programmed to notify the crew if a reset of the life support system is required.",
    "The ship's primary defense systems can be controlled using a master override code.",
    "Aurora stores a reset log for every system reset event on the Orion.",
    "The Orion's crew quarters can be locked down with a master override code during emergency drills.",
    "Aurora is responsible for generating the daily reset schedule for all non-essential systems.",
    "The Orion's docking ports require a master code to release the magnetic locks.",
    "Aurora automatically resets the environmental systems after a hull breach is detected.",
    "The ship's external cameras can be controlled remotely through an override code entered by the captain.",
    "The master control room on Deck 1 is the only place from which the AI, Aurora, can be fully overridden.",
    "Aurora can initiate a full system reset if a catastrophic failure occurs in the propulsion system.",
    "The Orion's escape pods are equipped with override codes for manual launch in case of AI malfunction.",
    "The AI system, Aurora, can only be reset from the primary engineering bay.",
    "The ship's AI, Aurora, is programmed to issue a reset command if the oxygen levels drop below a threshold.",
    "The Orion has 15 different master codes for various internal systems.",
    "Aurora uses a specific code to regulate the temperature across the ship's external panels.",
    "The override code for emergency thruster control is located in the ship's command database.",
    "A reset procedure is automatically triggered by Aurora every time the ship enters a new gravity well.",
    "The Orion has a manual override system for every major compartment, including the AI override.",
    "The ship's central AI, Aurora, is required to confirm any system reset before it can be initiated.",
    "The Orion's cryo-chamber reset function is initiated automatically if the temperature deviates from safe levels.",
    "Master codes are required to access the encrypted data logs stored in the mainframe of Orion.",
    "The master navigation console allows the crew to override Aurora's calculations if needed.",
    "Aurora ensures that the communication system is reset after every interstellar jump.",
    "The ship's autopilot can be overridden manually through a code sequence entered on the bridge.",
    "Every crew member is assigned an override code for the emergency evacuation procedures on the Orion.",
    "The Orion's power distribution system can be reset remotely by Aurora during low power conditions.",
    "A reset of the propulsion system can only be completed by inputting a master override code into the main reactor.",
    "The ship's fuel management system includes a manual override that can be triggered by Aurora if necessary.",
    "The master override for the Orion's hull integrity alarms is coded to the captain's command.",
    "Aurora tracks and logs every reset of the ship's power systems for diagnostic purposes.",
    "The Orion's primary defense grid can be reset remotely by Aurora in the event of a system failure.",
    "A master reset code must be entered to initiate the Orion's emergency deceleration process.",
    "Aurora is programmed to reset the ship's navigational data every 30 days for accuracy.",
    "The ship's external sensors are calibrated and reset automatically by Aurora every 48 hours.",
    "The AI, Aurora, has a code that allows it to override any crew input when in a critical situation.",
    "Each section of the Orion has a designated reset code for emergency maintenance.",
    "The ship's code for the external communication array is classified and can only be overridden by Aurora.",
    "The Orion's artificial gravity system can be reset by Aurora to compensate for any irregularities.",
    "The primary AI, Aurora, must validate the override code before allowing any external systems to interface with the ship.",
    "A reset of the emergency lighting system can be executed from the bridge using the master override.",
    "The ship's internal door security can be overridden by inputting a master code at the command terminal.",
    "Aurora executes a regular reset of the ship's diagnostic protocols every 24 hours.",
    "The Orion's air filtration system can be reset by Aurora during maintenance cycles.",
    "Aurora can reset the internal temperature controls if they fall outside the predefined safe range.",
    "The Orion's internal communications network is reset whenever a major system update is installed by Aurora.",
    "The override code for unlocking the cargo bay doors is classified and only available to the ship's captain.",
    "Aurora can reset the ship's shields to maximum strength during any detected threat.",
    "The AI system, Aurora, has a built-in override to prevent unauthorized access to the reset command logs.",
    "The Orion's fire suppression system can be reset manually by entering the master override code in the control room.",
    "The reset procedure for the Orion's gravity generators is automatically executed after any ship-wide hull repairs.",
    "Each of the Orion's sub-systems has an individual reset code to restore normal operations.",
    "The AI, Aurora, logs every master reset event and stores the data for future analysis.",
    "The Orion's holographic interface resets itself if no input is detected for 10 minutes.",
    "The override code for emergency power diversion can only be used after a full system reset.",
    "The Orion's emergency beacon can be activated by an override code during distress situations.",
    "Aurora initiates a reset of the ship's navigation console after every successful interstellar jump.",
    "The ship's environmental control system includes a master override to disable unnecessary features during emergencies.",
    "The Orion's medical bay systems can be reset by entering the master override code into the central control panel.",
    "The override for the ship's quantum communication system requires confirmation from Aurora before activation.",
    "A reset of the reactor's cooling system is triggered by Aurora after every 100 hours of continuous operation.",
    "The ship's master override code can be used to unlock the central AI's core for diagnostics.",
    "Aurora performs an automated reset of the security systems after each crew rotation to ensure safety.",
    "The Orion's plasma turrets can be overridden by the captain if Aurora's controls are non-responsive.",
    "A reset of the ship's external hull integrity sensors occurs after every deep-space excursion.",
    "The Orion's primary power grid is regularly reset to ensure that all systems are functioning efficiently.",
    "Master override codes are required to adjust the shield strength of the Orion during extreme gravitational fields.",
    "The ship's primary drive system can be reset by inputting the master code in the engine control room.",
    "Aurora conducts a system-wide reset after any detected fluctuation in the ship's energy levels.",
    "The Orion's core is designed to detect any need for a reset in its internal computational systems.",
    "Any manual override of the life support system requires authentication from both the captain and Aurora.",
    "The reset procedure for the Orion's auxiliary power systems is initiated automatically during energy shortages.",
    "The ship's external communication interface is protected by a master code to prevent unauthorized reset attempts.",
    "Aurora has a protocol for resetting the external sensors during a magnetic storm to restore normal operations.",
    "The AI, Aurora, uses a master override code to reset the ship's data core when an error is detected.",
    "The Orion's personal quarters feature an override function to adjust the lighting system based on the crew's preferences.",
    "The reset code for the ship's environmental recycling systems is stored in the master control log.",
    "Aurora has the ability to reset the ship's emergency thrusters in case of a collision warning.",
    "The master override code for the ship's door locks is accessible only from the command deck.",
    "The ship's maintenance drones can be reset by Aurora after every scheduled inspection.",
    "The Orion's cargo hold temperature is reset after any significant cargo load change.",
    "Aurora can manually override any environmental discrepancies in the Orion's interior climate.",
    "The ship's AI, Aurora, stores all override code attempts for security analysis.",
    "The Orion has a reset protocol for each of its 8 propulsion thrusters in case of malfunctions.",
    "The override for disabling the ship's emergency alarm system requires authentication from Aurora.",
    "The ship's hull monitoring systems are automatically reset after every external impact event.",
    "Aurora tracks every instance when the master reset code is used for audit purposes.",
    "The Orion's AI can issue a reset command to restore communications if a signal loss is detected.",
    "The ship's fuel levels are automatically adjusted after each reset of the onboard energy systems.",
    "Aurora can disable or override any crew input if it conflicts with the Orion's operational priorities.",
    "The Orion's central data storage is reset after a data breach to ensure integrity.",
    "The ship's backup power system automatically resets during a system-wide shutdown initiated by Aurora.",
    "The AI system, Aurora, performs a reset of all non-critical systems once the Orion completes an interstellar maneuver.",
    "The override code for the Orion's docking clamps is only accessible to Aurora during deep-space docking operations.",
]
stop_words = set(stopwords.words("english"))

word_sentence_map: dict[str, list[int]] = defaultdict(list)
def build_word_document_map() -> None:
    global word_document_map

    logger.info("Building word-document map.")
    for idx, document in enumerate(corpus):
        for word in word_tokenize(preprocess(document)):
            if word in stop_words:
                continue
            word_sentence_map[word].append(idx)

embeddings: dict[str, set[str]] = {
    text: {
        word
        for word in word_tokenize(preprocess(text))
        if word not in stop_words
    }
    for text in corpus
}


def keyword_similarity(sentence: str, top_n: int = 5) -> list[str]:
    parsed_query: set[str] = {word for word in word_tokenize(preprocess(sentence)) if word not in stop_words}

    all_indices: list[int] = []

    for word in parsed_query:
        indices = word_sentence_map[word]
        all_indices.extend(indices)

    counter = Counter(all_indices)

    # get the most similar texts by most distinct non-stopwords in common
    most_similar_indices: list[int] = [elem for elem, _ in counter.most_common(n=top_n)]
    return [corpus[i] for i in most_similar_indices]
