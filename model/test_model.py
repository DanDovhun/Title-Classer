import joblib
import numpy as np
import re
import spacy
from model import preprocess_text

# Load the model and vectorizer
model = joblib.load("model.joblib")
vectorizer = joblib.load("vectorizer.joblib")

titles = [
    # medium articles:
    ["Intro to LLM Agents with Langchain: When RAG is Not Enough", 2],
    ["Disruption Comes to Google", 2],
    ["How to change your city through a ballot measure", 2],

    #Sports
    ["Nepotism in sports broadcasting: ‘A tremendous advantage,’ but ‘what do you do with it?’", 1],
    ["Carragher, Abdo and the verbal grenade on CBS that made everyone squirm", 1],
    ["A mysterious illness halted his promising NHL career. Eight years later, hope and a comeback", 1],

    #  Politics
    ["Diverse cabinet is no ‘get-out-of-jail-free card’ on racism, says ex-No 10 adviser", 0],
    ["‘Complex’ post-Brexit tax rules means price rises for UK wine drinkers", 0],
    ["Post-2019 UK cabinet ministers last average of eight months, study finds", 0],
]

articles = [
    ["Hello everyone, this article is a written form of a tutorial I conducted two weeks ago with Neurons Lab. If you prefer a narrative walkthrough, you can find the YouTube video here:", 2],
    ["The tech industry is extremely dynamic and the only constant is change. Companies that once appeared to be invulnerable can be regularly upset by upstarts unless they adapt. We can see this in the difference in fortunes between Microsoft and Intel which both saw the PC displaced by mobile devices. Microsoft adapted by pivoting to the cloud while Intel’s fortunes have declined as ARM, TSMC and Nvidia are ascendant..", 2],
    ["In late 2021, I was frustrated. I had started Streets For All two years earlier, in 2019, to make Los Angeles a more multimodal city. When I started, I didn’t know anything about how local government worked, or how decisions were made. I just knew my City — Los Angeles — was broken from a street safety point of view, and I wanted to change it. In 2019 I had come across the City of Los Angeles Mobility Plan 2035, a visionary plan that the City had adopted in 2015 as the transportation element of their general plan — every city, per state law, has to have a general plan that covers things like land use (zoning) and transportation.", 2],

    #sports
    ["When Jac Collinsworth, at just 27 years old, debuted on the prestigious job as NBC’s play-by-play voice for Notre Dame football in September 2022, he succeeded one of the most decorated announcers in sports, Mike Tirico. To receive such a position suggested he was a sportscasting prodigy, but from his first game — when Marshall upset Notre Dame — Collinsworth did not sound like he deserved the national stage in this role. He lacked precision and rhythm, and he kept saying, “Mmm, hmm,” a bad habit that usually is eradicated with years of practice.", 1],
    ["When Micah Richards isn’t laughing, you know you’re in trouble. Jamie Carragher’s dig at Kate Abdo, lobbing a verbal grenade appearing to jokingly suggest that she wasn’t faithful to her partner Malik Scott, made for tough watching. If you watched it on CBS Sports Golazo during its coverage of Arsenal against Porto in the Champions League, you’ll instantly recall the cringe. You may have screwed up your face, you may have covered your eyes, you may have put your t-shirt over your head, Fabrizio Ravanelli style.", 1],
    ["The game was already won when the puck slid to Cody Hodgson for the tap-in. The Milwaukee Admirals of the American Hockey League, the Nashville Predators’ top minor league affiliate, had a comfortable 3-0 lead over the Chicago Wolves. On a historic win streak — they were en route to their 18th consecutive victory — the Admirals juggled their lines. Off of a rush chance in the final minute, Predators prospect Juuso Pärssinen pulled off a slick toe-drag deke and waited patiently for a lane to open up. Then he feathered a perfect pass to Hodgson for the goal.", 1],

    #Politics
    ["A former Downing Street race adviser has warned the government not to use its diversity as a “get-out-of-jail-free card” on tackling racism after a senior minister denied that the Conservatives had a problem after the Frank Hester row.Samuel Kasumu, a former No 10 adviser on civil society and communities, said he was “frustrated and disappointed” by the party’s response to the scandal, adding: “I know that we can do better.”", 0],
    ["British consumers have been told that the price of some of their favourite red wines could increase by more than 40p next year after the government ignored pleas from the wine industry to abandon complex post-Brexit tax changes. The chief executive of Majestic Wine, John Colley, said the new alcohol duty system, which comes into effect in February 2025, would increase the number of tax bands for wine from one to 30, and cost businesses huge sums of money to administer.", 0],
    ["Cabinet ministers in the UK’s post-2019 parliament have lasted in their jobs for an average of just eight months, a report comparing political stability across 17 countries has found, with Westminster also faring badly on a series of other metrics.The study, Strong and Stable, which looked at 10 aspects of parliamentary and governmental stability in countries using various electoral systems over the past 50 years, concluded that proportional voting did not mean more volatility compared with UK-style systems, and often the contrary.", 0]
]

nlp = spacy.load("en_core_web_sm")

categories = {
    "0": "Politics",
    "1": "Sport",
    "2": "Technology",
    "3": "Entertainment",
    "4": "Business"
}

# Preprocess text
for i in range(0,len(titles)):
    titles[i][0] = preprocess_text(titles[i][0])
    articles[i][0] = preprocess_text(articles[i][0])

correctTitles = 0
correctArticles = 0

print("titles")
for i in titles:
    reshaped = np.array([i[0]])
    transformed = vectorizer.transform(reshaped)
    prediction = model.predict(transformed)
    cat = categories[str(prediction[0])]

    print(f"Category: {cat}")

    if prediction == i[1]:
        correctTitles += 1

print("\narticles")
for i in articles:
    reshaped = np.array([i[0]])
    transformed = vectorizer.transform(reshaped)
    prediction = model.predict(transformed)
    cat = categories[str(prediction[0])]

    print(f"Category: {cat}")

    if prediction == i[1]:
        correctArticles += 1

print()
print(f"Correctly classified titles: {correctTitles} ({100 * correctTitles / len(titles)}%)")
print(f"Correctly classified articles: {correctArticles} ({100 * correctArticles / len(articles)}%)")