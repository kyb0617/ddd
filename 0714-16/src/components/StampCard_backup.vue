<script setup>

import {ref, onMounted, onActivated} from "vue"

import cardCommon from "../assets/images/card_common.png"
import cardAdvanced from "../assets/images/card_advanced.png"
import cardRare from "../assets/images/card_rare.png"
import cardLegendary from "../assets/images/card_legendary.png"

const props = defineProps({

  stamp: Object

})

function cardImage(){

    if(props.stamp.rarity==="common"){
        return cardCommon
    }

    if(props.stamp.rarity==="advanced"){
        return cardAdvanced
    }

    if(props.stamp.rarity==="rare"){
        return cardRare
    }

    return cardLegendary

}

const distance = ref(null)

const canGetStamp = ref(false)

const isCollected = ref(false)

const showPopup = ref(false)

function getLocation(){

showPopup.value = true  

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

showPopup.value = false

}

function closePopup(){

    showPopup.value = false

}

function resetStamps(){

localStorage.removeItem("myStamps")

isCollected.value = false

location.reload()

}

function rarityName(rarity){

  if(rarity === "common"){
    return "일반"
  }

  if(rarity === "advanced"){
    return "고급"
  }

  if(rarity === "rare"){
    return "희귀"
  }

  if(rarity === "legendary"){
    return "전설"
  }

  return rarity

}


function rarityIcon(rarity){

  if(rarity === "common"){
    return "🟢"
  }

  if(rarity === "advanced"){
    return "🔷"
  }

  if(rarity === "rare"){
    return "🔴"
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

<div class="stamp-card" :class="stamp.rarity">

  <img
  class="card-bg"
  :src="cardImage()"
/>

  <!-- 이미지 -->
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
      도장
    </div>

  </div>

  <!-- 장소 이름 -->
  <h2>
    {{ stamp.place }}
  </h2>

  <!-- 희귀도 -->
  <div class="rarity">

    {{ rarityIcon(stamp.rarity) }}
    {{ rarityName(stamp.rarity) }}

  </div>

  <!-- 정보 -->
  <div class="condition">

    <p>

      <span>💎 가치</span>

      <span>{{ stamp.weight }}</span>

    </p>

    <p>

      <span>📍 위치</span>

      <span>{{ stamp.condition.distance }}m</span>

    </p>

    <p>

      <span>🌤 날씨</span>

      <span>{{ stamp.special.weather }}</span>

    </p>

    <p>

      <span>🕒 시간</span>

      <span>{{ stamp.special.time }}</span>

    </p>

  </div>

  <!-- 상태 -->
  <div class="status">

    <template v-if="isCollected">

      ✅ 획득 완료

    </template>

    <template v-else>

      🔒 미획득

    </template>

  </div>

  <!-- 버튼 -->
  <button @click="getLocation">

    📍 위치 확인

  </button>

</div>

<!-- =========================
      팝업
========================== -->

<div
  v-if="showPopup"
  class="popup-overlay"
  @click.self="closePopup"
>

  <div class="popup">

    <h3>

      {{ stamp.place }}

    </h3>

    <p>

      현재 거리 :
      {{ distance }}m

    </p>

    <template v-if="isCollected">

      <p class="success">

        ✅ 이미 획득한 도장입니다.

      </p>

    </template>

    <template v-else>

      <template v-if="canGetStamp">

        <p class="success">

          ✨ 도장 획득 가능!

        </p>

        <button @click="getStamp">

          🏷️ 도장 획득

        </button>

      </template>

      <template v-else>

        <p class="fail">

          🔒 아직 멀었습니다.

        </p>

      </template>

    </template>

    <button
      class="close-btn"
      @click="closePopup"
    >

      닫기

    </button>

  </div>

</div>

</template>


<style scoped>
:root{

  --paper:#F5E5BF;
  --paper2:#EFD5A5;

  --brown:#5A3C1C;
  --dark:#3B2712;

  --common:#4CAF50;
  --rare:#3B82F6;
  --advanced:#A855F7;
  --legend:#F59E0B;

}

.stamp-card{

    position:relative;

    width:320px;

    margin:28px;

    overflow:hidden;

    background:url("../assets/images/parchment.jpg") center/cover no-repeat;

    border:5px solid var(--dark);

    border-radius:6px;

    color:var(--brown);

    box-shadow:
        6px 6px 0 #654321,
        12px 12px 20px rgba(0,0,0,.28);

    transition:.18s;

}

.stamp-card:hover{

    transform:translateY(-6px);

    box-shadow:
        8px 8px 0 #654321,
        16px 16px 25px rgba(0,0,0,.35);

}

/* ===========================
   희귀도별 테두리
=========================== */

.stamp-card.common{

    border-color:#2E8B57;

}

.stamp-card.advanced{

    border-color:#2563EB;

}

.stamp-card.rare{

    border-color:#DC2626;

}

.stamp-card.legendary{

    border-color:#F59E0B;

}

/* ===========================
      이미지 영역
=========================== */

.image-area{

    display:flex;

    justify-content:center;

    align-items:center;

    padding-top:28px;

    padding-bottom:18px;

}

/* 원형 메달 */

.stamp-image{

    width:180px;

    height:180px;

    border-radius:50%;

    object-fit:cover;

    border:6px solid #8A5A2B;

    background:white;

    box-shadow:

        0 0 0 5px #DDB56E,

        5px 5px 0 rgba(0,0,0,.18);

}

/* 이미지 없을 때 */

.empty-image{

    width:180px;

    height:180px;

    border-radius:50%;

    border:5px dashed #9C6A34;

    display:flex;

    align-items:center;

    justify-content:center;

    flex-direction:column;

    background:#FFF7E5;

    font-size:22px;

}

/* ===========================
       장소 이름
=========================== */

h2{

    margin:0;

    padding:18px 12px;

    font-size:25px;

    text-align:center;

    background:rgba(255,255,255,.55);

}

/* ===========================
      희귀도 리본
=========================== */

.rarity{

    padding:14px;

    text-align:center;

    color:white;

    font-size:22px;

    letter-spacing:2px;

}

.stamp-card.common .rarity{

    background:#2E8B57;

}

.stamp-card.advanced .rarity{

    background:#2563EB;

}

.stamp-card.rare .rarity{

    background:#DC2626;

}

.stamp-card.legendary .rarity{

    background:#F59E0B;

}

/* ===========================
      정보 박스
=========================== */

.condition{

    margin:22px;

    padding:18px;

    background:rgba(255,255,255,.72);

    border:3px solid #D7B06C;

}

.condition p{

    display:flex;

    justify-content:space-between;

    margin:12px 0;

    font-size:17px;

}

/* ===========================
        가치
=========================== */

.weight{

    display:flex;

    justify-content:space-between;

    font-size:22px;

    margin-bottom:20px;

}

/* ===========================
       상태
=========================== */

.status{

    margin:22px;

    padding:18px;

    text-align:center;

    background:rgba(255,248,220,.65);

    border:3px solid #D7B06C;

    font-size:20px;

}

/* ===========================
        버튼
=========================== */

button{

    width:calc(100% - 40px);

    margin:0 20px 20px;

    padding:15px;

    font-size:22px;

    font-family:inherit;

    color:white;

    background:#A96B35;

    border:4px solid #6D421B;

    cursor:pointer;

    transition:.15s;

}

button:hover{

    background:#BF7A3D;

}

button:active{

    transform:translateY(2px);

}

/* ===========================
      팝업 안 버튼
=========================== */

.popup button{

    width:180px;

    margin:10px auto;

    display:block;

}

/* ===========================
      거리 표시
=========================== */

.distance{

    text-align:center;

    margin-bottom:18px;

    font-size:18px;

    color:#7A4B1E;

}

/* ===========================
      팝업
=========================== */

.popup-overlay{

    position:fixed;

    top:0;
    left:0;

    width:100vw;
    height:100vh;

    background:rgba(0,0,0,.55);

    display:flex;

    justify-content:center;

    align-items:center;

    z-index:9999;

}

.popup{

    width:340px;

    padding:24px;

    background:url("../assets/images/parchment.jpg") center/cover no-repeat;

    border:5px solid #6D421B;

    box-shadow:
        8px 8px 0 #654321,
        14px 14px 24px rgba(0,0,0,.35);

    text-align:center;

    color:#5A3C1C;

}

.popup h3{

    margin-top:0;

    margin-bottom:20px;

    font-size:24px;

}

.popup p{

    margin:14px 0;

    font-size:18px;

}

.success{

    color:#1E8E3E;

}

.fail{

    color:#C62828;

}

.close-btn{

    background:#777;

    border-color:#555;

}

.close-btn:hover{

    background:#666;

}

/* 획득 가능 상태 */

.success{

    color:#2E8B57;

    font-size:20px;

    font-weight:bold;

    text-shadow:
        0 0 4px #FFF7A5,
        0 0 8px #FFD700;

    animation:pulse .8s infinite alternate;

}

/* 반짝이는 애니메이션 */

@keyframes pulse{

    from{

        transform:scale(1);

    }

    to{

        transform:scale(1.08);

    }

}

.card-bg{

    width:100%;

    display:block;

}

</style>