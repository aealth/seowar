function updateAdmi(p1,p2,p3,p4){
  var p1Admi='MB'+p1.admission;
  var p2Admi='MB'+p2.admission;
  var p3Admi='MB'+p3.admission;
  var p4Admi='MB'+p4.admission;
  var MBC1=document.getElementById('MBC1');
  var MBC2=document.getElementById('MBC2');
  var MBC3=document.getElementById('MBC3');
  var MBC4=document.getElementById('MBC4');
  MBC1.parentNode.removeChild(MBC1);
  MBC2.parentNode.removeChild(MBC2);
  MBC3.parentNode.removeChild(MBC3);
  MBC4.parentNode.removeChild(MBC4);
  document.getElementById(p1Admi).appendChild(MBC1);
  document.getElementById(p2Admi).appendChild(MBC2);
  document.getElementById(p3Admi).appendChild(MBC3);
  document.getElementById(p4Admi).appendChild(MBC4);
}
function updatePlayerStat(data,pid){
  var stat='You are using '+data["players"][pid].university+' University rf='+data["players"][pid].rf+' cr='+data["players"][pid].cr+' cs='+data["players"][pid].cs+' ss='+data["players"][pid].ss+' | This is '+data["round_queue"][0]+' turn now.'
  ;
  document.getElementById('playerStatPanel').innerHTML=stat;
  console.log(JSON.stringify(data["players"][pid], null, 2));
}
function updateCardPanel(data,pid,cards){
  var cardOnhand=data["players"][pid].cards;
  document.getElementById('cardSelList').innerHTML='';
  //console.log(cardOnhand[0]);
  for (i=0;i<=10;i++){
    var cardNum=cardOnhand[i];
    if (cardNum!=null){
      var selectCard=document.createElement('option');
      selectCard.innerHTML=cards[cardNum].name;
      setAttributes(selectCard,{'value':cardNum,'onclick':'displayCard(this.value)'});
      //selectCard.setAttribute();
      document.getElementById('cardSelList').appendChild(selectCard);
    }
  }
}

function displayCard(cardNum){
  document.getElementById('cardDisPanel').innerHTML='<center><h4>'+cards[cardNum].name+'</h4><h6>'+cards[cardNum].description+'</h6><h6>RF: '+cards[cardNum].stat[0]+' CR: '+cards[cardNum].stat[1]+' CS: '+cards[cardNum].stat[2]+' SS: '+cards[cardNum].stat[3]+'</h6><h5>'+cards[cardNum].type+'</h5></center>';
}
function setAttributes(el, attrs) {
  for(var key in attrs) {
    el.setAttribute(key, attrs[key]);
  }
}
function displayPlayer(pid){
  var stat='<center><h4>'+data["players"][pid].university+' University</h4><h6>RF: '+data["players"][pid].rf+'</h6><h6>CR: '+data["players"][pid].cr+'</h6><h6>CS: '+data["players"][pid].cs+'</h6><h6>SS: '+data["players"][pid].ss+'</h6></center>';
  document.getElementById('playerDisPanel').innerHTML=stat;
}
function updateRank(p1,p2,p3,p4){
  var p1Rank='rank'+p1.position;
  var p2Rank='rank'+p2.position;
  var p3Rank='rank'+p3.position;
  var p4Rank='rank'+p4.position;
  var MBR1=document.getElementById('MBR1');
  var MBR2=document.getElementById('MBR2');
  var MBR3=document.getElementById('MBR3');
  var MBR4=document.getElementById('MBR4');
  MBR1.parentNode.removeChild(MBR1);
  MBR2.parentNode.removeChild(MBR2);
  MBR3.parentNode.removeChild(MBR3);
  MBR4.parentNode.removeChild(MBR4);
  document.getElementById(p1Rank).appendChild(MBR1);
  document.getElementById(p2Rank).appendChild(MBR2);
  document.getElementById(p3Rank).appendChild(MBR3);
  document.getElementById(p4Rank).appendChild(MBR4);
}
/*
function playCard(){
  //var socket = io.connect('http://127.0.0.1:5000');
  socket.emit('join');
	a = 'play';
  c = document.getElementById('cardSelList').value;
	t = document.getElementById('playerSelList').value;
	socket.emit('move', pid, a, c, t);
}
function endPlay(){
  //var socket = io.connect('http://127.0.0.1:5000');
  socket.emit('join');
	a = 'end_play';
	socket.emit('move', pid, a);
}
function throwCard(){
  //var socket = io.connect('http://127.0.0.1:5000');
  socket.emit('join');
  a = 'throw';
	c = document.getElementById('cardSelList').value;
  socket.emit('move', pid, a, c);
}
function endThrow(){
  //var socket = io.connect('http://127.0.0.1:5000');
  socket.emit('join');
  a = 'end_throw';
  socket.emit('move', pid, a);
}
*/
