<script setup>

import {ref, onMounted, onActivated} from "vue"

const props = defineProps({

  stamp: Object

})


const distance = ref(null)

const canGetStamp = ref(false)

const isCollected = ref(false)

function getLocation(){

console.log(props.stamp)

navigator.geolocation.getCurrentPosition(

(position)=>{


const userLat =
position.coords.latitude


const userLng =
position.coords.longitude

console.log(
"user 위치",
userLat,
userLng
)


console.log(
"도장 위치",
props.stamp.location.lat,
props.stamp.location.lng
)

distance.value =
calculateDistance(

userLat,
userLng,
props.stamp.location.lat,
props.stamp.location.lng

)


// 획득 가능 여부 판단

if(distance.value <= props.stamp.condition.distance){

    canGetStamp.value = true

}else{

    canGetStamp.value = false

}


},


(error)=>{

console.log(error)

alert(
"위치 오류 : "
+ error.message
)

}

)


}



function calculateDistance(

lat1,

lon1,

lat2,

lon2

){


const R = 6371e3;


const rad =
Math.PI / 180;


const dLat =
(lat2-lat1)*rad;


const dLon =
(lon2-lon1)*rad;


const a =

Math.sin(dLat/2) *
Math.sin(dLat/2)

+

Math.cos(lat1*rad) *
Math.cos(lat2*rad)

*

Math.sin(dLon/2) *
Math.sin(dLon/2);



const c =

2 *

Math.atan2(

Math.sqrt(a),

Math.sqrt(1-a)

);



return Math.round(R*c);


}

function getStamp(){


let stamps =
JSON.parse(
localStorage.getItem("myStamps")
)
|| []



// 이미 가지고 있는지 확인

if(stamps.includes(props.stamp.id)){

alert("이미 획득한 도장입니다")

return

}


// 저장

stamps.push(props.stamp.id)


localStorage.setItem(
"myStamps",
JSON.stringify(stamps)
)



isCollected.value = true

window.dispatchEvent(
new Event("stampUpdated")
)

alert(
"✨ " 
+ props.stamp.place
+ " 도장 획득!"
)


}

function resetStamps(){

localStorage.removeItem("myStamps")

isCollected.value = false

location.reload()

}

function rarityName(rarity){

  if(rarity === "common"){
    return "COMMON"
  }

  if(rarity === "rare"){
    return "RARE"
  }

  if(rarity === "epic"){
    return "EPIC"
  }

  if(rarity === "legendary"){
    return "LEGENDARY"
  }

  return rarity

}


function rarityIcon(rarity){

  if(rarity === "common"){
    return "⚪"
  }

  if(rarity === "rare"){
    return "🔷"
  }

  if(rarity === "epic"){
    return "💜"
  }

  if(rarity === "legendary"){
    return "👑"
  }

  return "⭐"

}

function checkCollected(){

let stamps =
JSON.parse(
localStorage.getItem("myStamps")
)
|| []


if(stamps.includes(props.stamp.id)){

isCollected.value = true

}else{

isCollected.value = false

}

}

onMounted(()=>{


checkCollected()


})

window.addEventListener(
"storage",
()=>{

checkCollected()

}
)

</script>


<template>

<div
class="stamp-card"
:class="stamp.rarity"
>


<!-- 도장 이미지 영역 -->

<div class="image-area">


<img
v-if="stamp.image"
:src="stamp.image"
class="stamp-image"
/>


<div
v-else
class="empty-image"
>

🏷️
<br>
도장 이미지

</div>


</div>



<!-- 이름 -->

<h2>
{{ stamp.place }}
</h2>



<!-- 희귀도 -->

<div 
class="rarity"
>

{{ rarityIcon(stamp.rarity) }}

{{ rarityName(stamp.rarity) }}

</div>



<!-- 가치 -->

<p class="weight">

💎 가치 :
{{ stamp.weight }}

</p>



<!-- 조건 -->

<div class="condition">

<p>
📍 위치 조건 :
{{ stamp.condition.distance }}m 이내
</p>


<p>
🌤 날씨 :
{{ stamp.special.weather }}
</p>


<p>
⏰ 시간 :
{{ stamp.special.time }}
</p>


</div>



<!-- 상태 -->

<div class="status">

<p v-if="isCollected">

✅ 획득 완료

</p>


<p v-else>

🔒 미획득

</p>

</div>

<button @click="getLocation">

📍 위치 확인

</button>





<p v-if="distance">

현재 거리 :

{{distance}}m

</p>

<div v-if="distance">

<p v-if="distance && !canGetStamp && !isCollected">

🔒 아직 멀었습니다

</p>

<p v-if="canGetStamp && !isCollected">

✨ 도장 획득 가능!

</p>



<button
v-if="canGetStamp && !isCollected"
@click="getStamp"
>

🏷️ 도장 획득

</button>

</div>



</div>


</template>


<style scoped>


.stamp-card{


width:280px;

padding:20px;

margin:20px;

border-radius:20px;

background:#fff8e7;

border:3px solid #b8860b;

text-align:center;

box-shadow:0 5px 15px rgba(0,0,0,0.15);


}

/* 희귀도별 카드 디자인 */

.stamp-card.rare{

border-color:#3b82f6;

}


.stamp-card.epic{

border-color:#9333ea;

background:#f3e8ff;

}


.stamp-card.legendary{

border-color:#f59e0b;

background:#fff7d6;

box-shadow:0 0 20px gold;

}

.image-area{

height:180px;

display:flex;

justify-content:center;

align-items:center;

}

.empty-image{

width:150px;

height:150px;

border:3px dashed #b8860b;

border-radius:20px;

display:flex;

justify-content:center;

align-items:center;

flex-direction:column;

font-size:20px;

color:#8b4513;

background:#fff3cd;

}



.stamp-image{

width:150px;

height:150px;

object-fit:contain;

}



.rarity{

font-size:20px;

font-weight:bold;

margin:10px;

letter-spacing:2px;

}

.stamp-card.common .rarity{

color:#666;

}


.stamp-card.rare .rarity{

color:#2563eb;

}


.stamp-card.epic .rarity{

color:#9333ea;

}


.stamp-card.legendary .rarity{

color:#d97706;

}



.weight{

font-size:18px;

}



.condition{

margin-top:15px;

font-size:14px;

}



.status{

margin:15px;

font-size:18px;

}



button{

background:#8b4513;

color:white;

border:none;

padding:12px 25px;

border-radius:20px;

cursor:pointer;

}


button:hover{

opacity:0.8;

}


</style>