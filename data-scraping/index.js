import puppeteer from "puppeteer";
import ObjectsToCsv from "objects-to-csv";
// run with node index.js

const getmatches = async () => {
  // Start a Puppeteer session with:
  // - a visible browser (`headless: false` - easier to debug because you'll see the browser in action)
  // - no default viewport (`defaultViewport: null` - website page will be in full width and height)
  const browser = await puppeteer.launch({
    headless: true,
    defaultViewport: null,
  });

  // Open a new page
  const page = await browser.newPage();

  // On this new page:
  // - open the website
  // - wait until the dom content is loaded (HTML is ready)
  await page.goto(
    "https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryGame?MHG%5Bpreload%5D=Tournament&MHG%5Btournament%5D=LCK%2F2022+Season%2FSummer+Season&_run=",
    {
      waitUntil: "domcontentloaded",
    }
  );

  // Get page data

  const matches = await page.evaluate(() => {
    const matchList = document.querySelectorAll(".multirow-highlighter");
    console.log(matchList);
    // Convert the matchList to an iterable array
    // For each match fetch the text and author
    return Array.from(matchList).map((match) => {
      const dateText = match.firstChild.innerText;
      const blueTeamName = match.childNodes[2].querySelector("a").title;
      const redTeamName = match.childNodes[3].querySelector("a").title;
      const winnerName = match.childNodes[4].querySelector("a").title;

      const blueBan1 = match.childNodes[5].childNodes[0].title;
      const blueBan2 = match.childNodes[5].childNodes[1].title;
      const blueBan3 = match.childNodes[5].childNodes[2].title;
      const blueBan4 = match.childNodes[5].childNodes[3].title;
      const blueBan5 = match.childNodes[5].childNodes[4].title;

      const redBan1 = match.childNodes[6].childNodes[0].title;
      const redBan2 = match.childNodes[6].childNodes[1].title;
      const redBan3 = match.childNodes[6].childNodes[2].title;
      const redBan4 = match.childNodes[6].childNodes[3].title;
      const redBan5 = match.childNodes[6].childNodes[4].title;

      const bluePick1 = match.childNodes[7].childNodes[0].title;
      const bluePick2 = match.childNodes[7].childNodes[1].title;
      const bluePick3 = match.childNodes[7].childNodes[2].title;
      const bluePick4 = match.childNodes[7].childNodes[3].title;
      const bluePick5 = match.childNodes[7].childNodes[4].title;

      const redPick1 = match.childNodes[8].childNodes[0].title;
      const redPick2 = match.childNodes[8].childNodes[1].title;
      const redPick3 = match.childNodes[8].childNodes[2].title;
      const redPick4 = match.childNodes[8].childNodes[3].title;
      const redPick5 = match.childNodes[8].childNodes[4].title;

      // const blueBans = Array.from(
      //   match.childNodes[5].querySelectorAll("span")
      // ).map((ban) => ban.title);
      // const redBans = Array.from(
      //   match.childNodes[6].querySelectorAll("span")
      // ).map((ban) => ban.title);

      // const bluePicks = Array.from(
      //   match.childNodes[7].querySelectorAll("span")
      // ).map((ban) => ban.title);
      // const redPicks = Array.from(
      //   match.childNodes[8].querySelectorAll("span")
      // ).map((ban) => ban.title);

      const blueTop = match.childNodes[9].childNodes[0].innerText;
      const blueJng = match.childNodes[9].childNodes[2].innerText;
      const blueMid = match.childNodes[9].childNodes[4].innerText;
      const blueAdc = match.childNodes[9].childNodes[6].innerText;
      const blueSup = match.childNodes[9].childNodes[8].innerText;

      const redTop = match.childNodes[10].childNodes[0].innerText;
      const redJng = match.childNodes[10].childNodes[2].innerText;
      const redMid = match.childNodes[10].childNodes[4].innerText;
      const redAdc = match.childNodes[10].childNodes[6].innerText;
      const redSup = match.childNodes[10].childNodes[8].innerText;

      // const blueRoster = Array.from(
      //   match.childNodes[9].querySelectorAll("a")
      // ).map((ban) => ban.innerText);
      // const redRoster = Array.from(
      //   match.childNodes[10].querySelectorAll("a")
      // ).map((ban) => ban.innerText);

      return {
        dateText,
        blueTeamName,
        redTeamName,
        winnerName,
        blueBan1,
        blueBan2,
        blueBan3,
        blueBan4,
        blueBan5,
        redBan1,
        redBan2,
        redBan3,
        redBan4,
        redBan5,
        bluePick1,
        bluePick2,
        bluePick3,
        bluePick4,
        bluePick5,
        redPick1,
        redPick2,
        redPick3,
        redPick4,
        redPick5,
        blueTop,
        blueJng,
        blueMid,
        blueAdc,
        blueSup,
        redTop,
        redJng,
        redMid,
        redAdc,
        redSup,
        // redBans,
        // bluePicks,
        // redPicks,
        // blueRoster,
        // redRoster,
      };
    });
  });

  // Display the matches
  console.log(matches);
  (async () => {
    const csv = new ObjectsToCsv(matches);
    // Save to file:
    await csv.toDisk("./matches.csv");
  })();

  // Close the browser
  await browser.close();
};

// Start the scraping
getmatches();