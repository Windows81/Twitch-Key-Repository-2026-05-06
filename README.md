# Twitch Key Repository
I've amassed collection of publicly available Twitch stream keys; tested one-by-one on 2026-05-05.

## How to Reproduce
Navigate to GitHub, then use your browser's DevTools to run the following scripts in succession:

<details> 
<summary>(1)</summary>

```js
var r = [];
var QUERIES = [
	"stream /live_[1][01][0-9]{4,}_[a-z0-9]{30}/",
	"stream /live_[1][234][0-9]{4,}_[a-z0-9]{30}/",
	"stream /live_[1][567][0-9]{4,}_[a-z0-9]{30}/",
	"stream /live_[1][89][0-9]{4,}_[a-z0-9]{30}/",
	"stream /live_[234][0-9][0-9]{4,}_[a-z0-9]{30}/",
	"stream /live_[56][0-9][0-9]{4,}_[a-z0-9]{30}/",
	"stream /live_[789][0-9][0-9]{4,}_[a-z0-9]{30}/",
	"/live_[1][0-9][0-9]{4,}_[a-z0-9]{30}/ NOT stream",
	"/live_[234][0-9][0-9]{4,}_[a-z0-9]{30}/ NOT stream",
	"/live_[56][0-9][0-9]{4,}_[a-z0-9]{30}/ NOT stream",
	"/live_[789][0-9][0-9]{4,}_[a-z0-9]{30}/ NOT stream",
];
console.log("Running...");
for (let query of QUERIES) {
  for (let i = 1; i <= 5; ++i) {
    var url = `https://github.com/search?q=${encodeURIComponent(query)}&ref=opensearch&type=code&p=${i}`;
    var response = await fetch(url, {
      headers: {
        accept: "application/json",
        "accept-language": "en-GB,en;q=0.9,es;q=0.8",
        priority: "u=1, i",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "x-github-target": "dotcom",
        "x-react-router": "json",
        "x-requested-with": "XMLHttpRequest",
      },
      body: null,
      method: "GET",
      mode: "cors",
      credentials: "include",
    });

    var j = await response.json();
    var appended = Array.from(
      j.payload.results
        .flatMap((e) => e.snippets.flatMap((e) => e.lines))
        .join("")
        .matchAll("live_[0-9]{7,10}_[a-zA-Z0-9]{20,}"),
    ).map((e) => e[0]);
    r.push.apply(r, appended);
  }
}
console.log("Finished!");
```
</details>

...then, once `"Finished!"` is printed, copy the result ...


<details> 
<summary>(2)</summary>

```js
copy(r.join('\n'))
```
</details>

Then download and run [`test-twitch.py`](./test-twitch.py), making sure to have installed the `requests` library.  Paste the lines you just copied into the program's standard input.

The output will look similar to [`twitch-keys.txt`](./twitch-keys.txt).
