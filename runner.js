const { Builder, By, Key, until } = require("selenium-webdriver");

(async function example() {
  let driver = await new Builder().forBrowser("safari").build();
  try {
    await driver.get("http://hypem.com");
    await driver.findElement(By.linkText("Log in")).click();
    await driver.findElement(By.id("user_screen_name")).sendKeys("username");
    await driver.findElement(By.id("user_password")).sendKeys("password");
    await driver.findElement(By.id("defaultForm")).submit();
    await driver.get("https://hypem.com/popular/lastweek");
    console.log(driver.getPageSource());
  } finally {
    await driver.quit();
  }
})();
