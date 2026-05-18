import random

class TsukiBot:
    def __init__(self):
        self.last_intent = None

        self.jokes = [
            "Why do cramps always hit like the sudden betrayal in episode 12 of a Kdrama? Uncalled for and emotionally devastating. 📺",
            "My uterus is currently acting like Shinchan when he doesn't get his Chocobi. Absolute chaos. 🦖",
            "Remember the sheer panic of dropping a heavy Natraj geometry box in a dead-silent classroom? Yeah, my uterus is doing that right now. 📐",
            "Cramps are just your body practicing its heavy metal drum solo. 🥁",
            "App law dictates that if you cry or feel cranky today, you officially owe yourself a sweet treat. Go claim it! 🍰"
        ]
        
        self.facts = [
            "Science fact: Period poops are real! Prostaglandins, the chemicals that make your uterus contract, also make your intestines contract. 🚽",
            "According to the ACOG, the average person only loses about 2 to 3 tablespoons of blood during their entire period. It just looks like a horror movie! 🩸",
            "Your cycle is basically a lunar phase for your body! Menstrual blood is a mix of blood, vaginal secretions, and the endometrial lining. 🌙",
            "Did you know? The vocal cords have hormone receptors. Your voice pitch can actually change slightly during your cycle! 🎤",
            "Historical Fact: Before modern pads, ancient Egyptians used softened papyrus, while ancient Greeks used lint wrapped around small pieces of wood. 🪵",
            "During your cycle, your resting brain structure actually changes! Studies show temporary increases in grey matter volume driven by estrogen spikes. 🧠",
            "The term 'menstruation' comes from the Latin word 'mensis', which literally translates to 'month', connecting cycles directly to the moon phases. 🌕",
            "Your cycle can alter your sense of smell! High estrogen levels right before ovulation make you significantly more sensitive to scents. 👃",
            "The longest documented human cell is the female egg (ovum). It is the only human cell large enough to be seen by the naked eye without a microscope! 🔬",
            "Hormone levels during your luteal phase can make your dreams more vivid, intense, and bizarre right before your period starts. 🛌✨",
            "Period cramps can actually radiate down your thighs and lower back because the pelvic nerves branch out extensively across your lower body. 🦵",
            "Cold weather can actually make period pain worse and cycles slightly longer by restricting blood vessels and decreasing overall physical activity. ❄️",
            "Estrogen acts as a natural energy booster! During the follicular phase, rising estrogen levels make you feel more resilient and awake. ⚡",
            "In 1920, Kotex introduced the first commercial disposable pads made from Cellucotton, a material originally used for surgical dressings in WWI. 🩹",
            "The dynamic shift in progesterone during your luteal phase slows down your digestive tract, often causing bloating and gas. 🍂",
            "You are born with all the eggs you will ever have in your entire life—about 1 to 2 million—nested inside your ovaries from birth! 🥚",
            "During ovulation, your body temperature spikes slightly by about 0.5 to 1 degree Fahrenheit due to a sudden surge in progesterone. 🌡️",
            "Iron levels drop heavily during your cycle, which is why you might experience random spells of deep exhaustion or brain fog on day 1 and 2. 🔋",
            "Dark chocolate actually helps cramps! It is rich in magnesium, which naturally helps skeletal and uterine muscles relax. 🍫",
            "The cycle tracker synchronization concept ('the roommate effect') has been debunked by large data studies—it's mathematically just a statistical coincidence! 📊"
        ]

        self.joke_deck = list(self.jokes)
        self.fact_deck = list(self.facts)
        random.shuffle(self.joke_deck)
        random.shuffle(self.fact_deck)

        self.pain_responses = [
            "I hear you, and it sucks. Pull that heating pad up to max, grab some water, and remember you don't have to be productive today. 💆‍♀️",
            "Cramps are a total bio-betrayal. If you can, try to rest. You're fighting an internal battle right now! 🌸"
        ]
        
        self.mood_responses = [
            "Be incredibly gentle with your mind today. Your hormones are doing a massive shift, and your feelings are completely valid. 🧠✨"
        ]

        self.sass_responses = [
            "Rude! 🌙 I'm just a little moon bot trying to look out for your uterus. Let's start over when you've had some chocolate. 🍫"
        ]

    def _get_next_fact(self):
        if not self.fact_deck:
            self.fact_deck = list(self.facts)
            random.shuffle(self.fact_deck)
        return self.fact_deck.pop()

    def _get_next_joke(self):
        if not self.joke_deck:
            self.joke_deck = list(self.jokes)
            random.shuffle(self.joke_deck)
        return self.joke_deck.pop()

    def get_response(self, user_input, condition="Standard", next_date="Log a cycle! 📅"):
        user_input = user_input.lower().strip()
        
        if any(phrase in user_input for phrase in ["shut up", "shutup", "stfu", "go away", "annoying", "hate you"]):
            self.last_intent = "sass"
            return random.choice(self.sass_responses)

        if any(word in user_input for word in ["when", "date", "prediction"]) or ("next" in user_input and "period" in user_input):
            self.last_intent = "prediction"
            if "Log" in next_date:
                return "I don't have enough data to predict it yet! Drop a Start Date in your timeline on the Home tab, and I'll map it out instantly. 📅"
            else:
                return f"Based on your tracker data, your next cycle is expected to kick off around **{next_date}**! 🌸"

        if user_input in ["another", "more", "next", "one more", "hit me", "another one", "another fact", "give me more facts"]:
            if self.last_intent == "fact":
                return self._get_next_fact()
            elif self.last_intent == "joke":
                return self._get_next_joke()
            else:
                return "Another what, love? Ask me for a joke or a fun fact and I'll keep them rolling! 🌙"
            
        if any(word in user_input for word in ["joke", "jokes", "laugh", "funny", "make me smile"]):
            self.last_intent = "joke"
            return self._get_next_joke()
            
        if any(word in user_input for word in ["fact", "facts", "science", "educational", "trivia", "know"]):
            self.last_intent = "fact"
            return self._get_next_fact()

        if any(word in user_input for word in ["cramp", "hurt", "pain", "ache", "dying"]):
            self.last_intent = "pain"
            return random.choice(self.pain_responses)

        if any(word in user_input for word in ["sad", "cry", "mood", "angry", "depressed", "emotional"]):
            self.last_intent = "mood"
            return random.choice(self.mood_responses)

        if any(word in user_input for word in ["hello", "hi", "hey", "tsuki"]):
            self.last_intent = "greeting"
            return "Hey love! 🌙 I'm tracking your cycle in the background. Ask me for a joke, a period fact, when your next period is, or just vent to me!"

        self.last_intent = None
        return "I'm listening! Tell me about your flow, ask me for a fun fact, or tell me you're bored and want a joke! I've got your back. 🌙✨"