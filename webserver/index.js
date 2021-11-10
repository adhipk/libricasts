import express from "express";
import axios from "axios";
import dotenv from "dotenv";
import { PasteClient } from "pastebin-api";
const PORT = process.env.PORT || 3001;
const app = express();
dotenv.config({ silent: process.env.NODE_ENV === 'production' });
const pbClient = new PasteClient(process.env.PASTEBIN_API_KEY);
async function getRssFile(rssUrl) {
	// gets rss xml file from librevox
	const config = {
		method: 'GET',
		url: rssUrl,
	}
	const response = axios(config)
		.then(res => res.data)
		.catch(function (error) {
			console.log(error);
		});
	return response;

}
function fixPubdate(xml) {
	// uncomments pubdate field and replaces it with a random date.
	const regex = /<!--<pubDate>file element=rss.pubDate<\/pubDate>-->/gm;
	return xml.replace(regex, "<pubDate>Wed, 11 Nov 2021 20:17:21 +0100</pubDate>");
}

async function searchOldPastes(url) {
	// checks if url is already posted to pastebin and returns url 
	const userKey = process.env.PASTEBIN_USER;
	const pastes = await pbClient.getPastesByUser({
		userKey:userKey,
	});
	let match = pastes.find((paste)=>{
		return paste.paste_title == url;
	});
	return match?.paste_url ?? "";
	
}
async function UploadToPastebin(text,name){
	let match = await searchOldPastes(name);
	if(match){
		return match;
	}
	const url = await pbClient.createPaste({
		code: text,
		expireDate: "N",
		name: name,
		publicity: 1,
	});	
	return url;
}
async function uploadToPocketCasts(pastebinUrl, poll_id = '') {
	// sumbits patebin link to pocketcasts to create playlist

	var data = new URLSearchParams();
	data.append('url', pastebinUrl);
	data.append('poll_uuid', poll_id);
	var config = {
		method: 'post',
		url: 'https://refresh.pocketcasts.com/author/add_feed_url',
		headers: {
			'authority': 'refresh.pocketcasts.com',
			'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'origin': 'https://www.pocketcasts.com',
			'sec-fetch-dest': 'empty',
			'referer': 'https://www.pocketcasts.com/',
		},
		data: data,
		format: 'json',
	};

	let response = await axios(config)
		.then(response => response.data)
		.then(data => {
			if (data.status == 'poll') {
				// wait for 5 secs then retry with poll_uuid if response is poll

				return new Promise(resolve => setTimeout(resolve, 5000)).then(() => uploadToPocketCasts(pastebinUrl, data.poll_uuid).then(result => result));
			} else {
				return data;
			}
		})
		.catch(function (error) {
			console.log(error);
			return null;
		});

	return response?.result?.share_link ?? "";
}
app.get("/getUrl", async (req, res) => {
	let url = req.query.id ?? 'https://librivox.org/rss/16113';
	let rssFile = await getRssFile(url);
	let fixedRss = fixPubdate(rssFile);
	// add /raw to get just xml text
	let pastebinUrl = fixedRss ? await UploadToPastebin(fixedRss, url) : null;
	let pcUrl = pastebinUrl ? await uploadToPocketCasts(pastebinUrl.replace('.com/', '.com/raw/')) : null;

	res.json({
		url: pcUrl,
	})
});
app.get("/test", async (req, res) => {
	let result = await searchOldPastes('asd');
	res.json({'result':result});
})
app.listen(PORT, () => {
	console.log(`Server listening on ${PORT}`);
});
