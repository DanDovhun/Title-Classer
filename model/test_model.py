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
    ["What TF Did I Watch?: On Zola, Reesa Teesa, and Black Digital Storytelling", 2],
    ["I tasted the future of EV charging and it was delicious.", 2],

    #Sports
    ["Nepotism in sports broadcasting: ‘A tremendous advantage,’ but ‘what do you do with it?’", 1],
    ["Carragher, Abdo and the verbal grenade on CBS that made everyone squirm", 1],
    ["A mysterious illness halted his promising NHL career. Eight years later, hope and a comeback", 1],
    ["Fulham 3 Tottenham 0: Basic mistakes, confident Muniz and a missed opportunity – The Briefing", 1],
    ["Virgil van Dijk x LeBron James: The unlikely bond inspiring Liverpool’s captain", 1],

    #  Politics
    ["Diverse cabinet is no ‘get-out-of-jail-free card’ on racism, says ex-No 10 adviser", 0],
    ["‘Complex’ post-Brexit tax rules means price rises for UK wine drinkers", 0],
    ["Post-2019 UK cabinet ministers last average of eight months, study finds", 0],
    ["Millions more in cash needed to fund UK’s open-banking watchdog", 2],
    ["Victims of Norton Motorcycles pension fraud paid £9.4m compensation", 2]
]

articles = [
    ["Hello everyone, this article is a written form of a tutorial I conducted two weeks ago with Neurons Lab. If you prefer a narrative walkthrough, you can find the YouTube video here:", 2],
    ["The tech industry is extremely dynamic and the only constant is change. Companies that once appeared to be invulnerable can be regularly upset by upstarts unless they adapt. We can see this in the difference in fortunes between Microsoft and Intel which both saw the PC displaced by mobile devices. Microsoft adapted by pivoting to the cloud while Intel’s fortunes have declined as ARM, TSMC and Nvidia are ascendant..", 2],
    ["In late 2021, I was frustrated. I had started Streets For All two years earlier, in 2019, to make Los Angeles a more multimodal city. When I started, I didn’t know anything about how local government worked, or how decisions were made. I just knew my City — Los Angeles — was broken from a street safety point of view, and I wanted to change it. In 2019 I had come across the City of Los Angeles Mobility Plan 2035, a visionary plan that the City had adopted in 2015 as the transportation element of their general plan — every city, per state law, has to have a general plan that covers things like land use (zoning) and transportation.", 2],
    ["If you are anything like me, you have probably spent the last couple of weeks completely engrossed in the cautionary tale of Reesa Teesa. For those who are not chronically online, Reesa Teesa is a content creator on TikTok who recently shared a multi-video narrative of her marriage and divorce. The Who TF Did I Marry series comprises approximately 50 parts and over five hours of content. Reesa Teesa's story also warns about the dangers of dating while feeling desperate.", 2],
    ["Earlier this week I drove from Breckenridge back to San Francisco over the course of two days. Earlier this month, I did the same drive but in the other direction. The weather and traffic was variable—as was the quality of the innumerable podcasts I listened to—but there was one constant: I cursed Electrify America the whole way.", 2],

    #sports
    ["When Jac Collinsworth, at just 27 years old, debuted on the prestigious job as NBC’s play-by-play voice for Notre Dame football in September 2022, he succeeded one of the most decorated announcers in sports, Mike Tirico. To receive such a position suggested he was a sportscasting prodigy, but from his first game — when Marshall upset Notre Dame — Collinsworth did not sound like he deserved the national stage in this role. He lacked precision and rhythm, and he kept saying, “Mmm, hmm,” a bad habit that usually is eradicated with years of practice.", 1],
    ["When Micah Richards isn’t laughing, you know you’re in trouble. Jamie Carragher’s dig at Kate Abdo, lobbing a verbal grenade appearing to jokingly suggest that she wasn’t faithful to her partner Malik Scott, made for tough watching. If you watched it on CBS Sports Golazo during its coverage of Arsenal against Porto in the Champions League, you’ll instantly recall the cringe. You may have screwed up your face, you may have covered your eyes, you may have put your t-shirt over your head, Fabrizio Ravanelli style.", 1],
    ["The game was already won when the puck slid to Cody Hodgson for the tap-in. The Milwaukee Admirals of the American Hockey League, the Nashville Predators’ top minor league affiliate, had a comfortable 3-0 lead over the Chicago Wolves. On a historic win streak — they were en route to their 18th consecutive victory — the Admirals juggled their lines. Off of a rush chance in the final minute, Predators prospect Juuso Pärssinen pulled off a slick toe-drag deke and waited patiently for a lane to open up. Then he feathered a perfect pass to Hodgson for the goal.", 1],
    ["Tottenham Hotspur missed the opportunity to move into the top four after a 3-0 defeat to Fulham at Craven Cottage. Having recorded an impressive 4-0 victory over Aston Villa last time out, Spurs could have leapfrogged Unai Emery’s side into fourth with a win on Saturday. However, two goals from Rodrigo Muniz either side of a Sasa Lukic finish consigned Ange Postecoglou’s side to defeat and left them two points adrift of Villa.", 1],
    ["Liverpool captain Virgil van Dijk says he is inspired by the achievements of basketball legend LeBron James. Van Dijk and James, who is a minority shareholder in Liverpool’s owner Fenway Sports Group, recently joined forces for the launch of a new fashion range, LFC x LeBron, and have been exchanging messages indirectly.", 1],

    #Politics
    ["A former Downing Street race adviser has warned the government not to use its diversity as a “get-out-of-jail-free card” on tackling racism after a senior minister denied that the Conservatives had a problem after the Frank Hester row.Samuel Kasumu, a former No 10 adviser on civil society and communities, said he was “frustrated and disappointed” by the party’s response to the scandal, adding: “I know that we can do better.”", 0],
    ["British consumers have been told that the price of some of their favourite red wines could increase by more than 40p next year after the government ignored pleas from the wine industry to abandon complex post-Brexit tax changes. The chief executive of Majestic Wine, John Colley, said the new alcohol duty system, which comes into effect in February 2025, would increase the number of tax bands for wine from one to 30, and cost businesses huge sums of money to administer.", 0],
    ["Cabinet ministers in the UK’s post-2019 parliament have lasted in their jobs for an average of just eight months, a report comparing political stability across 17 countries has found, with Westminster also faring badly on a series of other metrics.The study, Strong and Stable, which looked at 10 aspects of parliamentary and governmental stability in countries using various electoral systems over the past 50 years, concluded that proportional voting did not mean more volatility compared with UK-style systems, and often the contrary.", 0],
    ["The Fraud Compensation Fund has paid £9.4m to the three retirement schemes that collapsed during the Norton Motorcycles pension scandal, more than a decade after victims had seemingly lost their life savings. The payment represents some long-awaited good news for more than 200 people who fell victim to what is known as “a pensions liberation fraud” during 2012 and 2013, when they were tricked into allowing about £11.5m to be transferred out of their existing retirement plans.", 0],
    ["Banks are under pressure to stump up millions of pounds in interim funding for the organisation that polices open banking, with regulators saying the new money is needed to prevent financial crime and protect consumers if things “go wrong”. Large banks including NatWest, HSBC, Lloyds and Santander UK were among more than 40 City firms summoned by the Financial Conduct Authority (FCA) last week to discuss a cash injection into Open Banking Limited (OPL), the body that oversees innovation in this area.", 0],
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