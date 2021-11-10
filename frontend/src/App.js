import './App.css';

import { useState } from 'react';
function App() {
	const pcSubmitUrl = 'https://refresh.pocketcasts.com/author/add_feed_url';
	const pbSubmitUrl = ''
	let [rssUrl,setRssUrl] = useState('');
	let [pastbinUrl,setpastbinUrl] = useState('');
	let [pocketCastsUrl,setPocketCastsUrl] = useState('');
	async function  getRssFile(){
		// gets rss xml file from librevox 
		const response = await fetch('https://cors-anywhere.herokuapp.com/'+rssUrl, {
			method:'GET',
			
		});
		let rawResponse = new XMLHttpRequest();
		rawResponse.open("GET",response,false);
		rawResponse.onreadystatechange = () => {
			if (rawResponse.readyState === 4) {
				if (rawResponse.status === 200 || rawResponse.status == 0) {
					var xmlasstring = rawResponse.responseText;
					console.log(xmlasstring);
					setPocketCastsUrl(xmlasstring);
				}
			}
		}
	}
	function fixPubdate(){
		// uncomments pubdate field and replaces it with a random date. 
	}
	async function UploadToPastebin(){
		// uploads corrected xml to pastebin 
	}
	async function uploadToPocketCasts(){
		// sumbits patebin link to pocketcasts to create playlist
	}
	function handleClick(){
		let rssFile = getRssFile();
		let fixedFile = fixPubdate(rssFile);
	}
	return (
		<div className="App">
			<h1>LibreCasts</h1>
			<h3>Enter rss feed url</h3>
			<input value = {rssUrl} onChange={(e)=>setRssUrl(e.target.value)}/>
			<button onClick={()=>handleClick()}>submit</button>
			{pocketCastsUrl ?? <a href={pocketCastsUrl}>{pocketCastsUrl}</a>}
		</div>
	);
}

export default App;
