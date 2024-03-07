let timeoutID;
let timeout = 1000;

const presentIDs = new Array();

function setup() {
	const tab = document.getElementById("chatbox");
	checkTable(tab);
	document.getElementById("sendButton").addEventListener("click", makePost);
    timeoutID = window.setTimeout(poller, timeout);
}

function checkTable(table){
	const chat_id = window.location.pathname.split("/")[2];
	fetch(`/messages/${chat_id}`)
		.then((response) => {
			return response.json();
		})
		.then((result)=>{
			for(var i = 0 ; i < result.length ; i++){
				console.log("type of first: "+typeof(result[i].message_id));
				presentIDs.push(result[i].message_id);
			}
		}).catch(()=>{
			console.log('error');
		})
}

function makePost(){
    const message = document.getElementById("message_text").value;
    const chat_id = window.location.pathname.split("/")[2];
    fetch(`/new_message/${chat_id}`,{
        method:"POST",
        headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
        body: `message=${message}`
    })
    .then((response) => {
        return response.json();
    })
    .then((result) => {

		updateChat(result);
        clearInput();
    })
    .catch(() => {
        console.log("Error posting new items!");
    });
}

function poller() {
	console.log("Polling for new items");
    const chat_id = window.location.pathname.split("/")[2];

	fetch(`/messages/${chat_id}`)
		.then((response) => {
			return response.json();
		})
		.then(updateChat)
		.catch(() => {
			window.location.href = "/lobby";
		});
}

function updateChat(result) {
	console.log("Updating the chat");
	for (let i = 0; i < result.length; i++) {
		if (presentIDs.includes(result[i].message_id)) {
		}else{
			addRow(result[i]);
			presentIDs.push(result[i].message_id);
		}
	}

	timeoutID = window.setTimeout(poller, timeout);
}

function addRow(row) {
	const tableRef = document.getElementById("chatbox");
	const newRow = tableRef.insertRow(-1);
	const newCell = newRow.insertCell(0);
	const text = row.author_id + ": "+row.text;
	const newText = document.createTextNode(text);
	newCell.appendChild(newText);
}

function clearInput() {
	console.log("Clearing input");
	document.getElementById("message_text").value = "";

}

window.addEventListener("load", setup);