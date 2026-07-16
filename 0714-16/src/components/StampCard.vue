<script setup>

import { ref, onMounted, computed } from "vue"

/* 카드 이미지 */

import cardCommon from "../assets/images/card_common.png"
import cardAdvanced from "../assets/images/card_advanced.png"
import cardRare from "../assets/images/card_rare.png"
import cardLegendary from "../assets/images/card_legendary.png"
import MudeungNationalPark from "../assets/images/place/MudeungNationalPark.png"
import acc from "../assets/images/place/acc.png"



/* Props */

const props = defineProps({

    stamp:Object,
    image:String

})


/* 카드 이미지 */

const cardImages={

    10:cardCommon,

    30:cardAdvanced,

    50:cardRare,

    80:cardLegendary

}

const cardImage = computed(()=>{

    return cardImages[props.stamp.weight]

})



/* 상태 */

const distance=ref(null)

const canGetStamp=ref(false)

const isCollected=ref(false)

const showPopup=ref(false)


/* 위치 확인 */

function getLocation(){

    console.log("버튼 클릭됨")

    navigator.geolocation.getCurrentPosition(

        (position)=>{

            console.log("GPS 성공")

            const userLat=position.coords.latitude

            const userLng=position.coords.longitude


            distance.value=calculateDistance(

                userLat,

                userLng,

                Number(props.stamp.lat),

                Number(props.stamp.lng)

            )


            canGetStamp.value=

                distance.value<=props.stamp.condition.distance

            console.log("팝업 열기")
            showPopup.value=true

        },

        (error)=>{

            alert("위치 오류 : "+error.message)

        }

    )

}


/* 거리 계산 */

function calculateDistance(

    lat1,

    lon1,

    lat2,

    lon2

){

    const R=6371e3

    const rad=Math.PI/180

    const dLat=(lat2-lat1)*rad

    const dLon=(lon2-lon1)*rad


    const a=

        Math.sin(dLat/2)**2+

        Math.cos(lat1*rad)*

        Math.cos(lat2*rad)*

        Math.sin(dLon/2)**2


    const c=2*Math.atan2(

        Math.sqrt(a),

        Math.sqrt(1-a)

    )


    return Math.round(R*c)

}


/* 획득 */

function getStamp(){

    let stamps=

    JSON.parse(

        localStorage.getItem("myStamps")

    )||[]


    if(stamps.includes(props.stamp.id)){

        alert("이미 획득한 도장입니다.")

        return

    }


    stamps.push(props.stamp.id)

    localStorage.setItem(

        "myStamps",

        JSON.stringify(stamps)

    )


    isCollected.value=true

    showPopup.value=false


    window.dispatchEvent(

        new Event("stampUpdated")

    )


    alert(

        "✨ "

        +props.stamp.place

        +" 도장 획득!"

    )

}


/* 팝업 */

function closePopup(){

    showPopup.value=false

}


/* 획득 여부 */

function checkCollected(){

    let stamps=

    JSON.parse(

        localStorage.getItem("myStamps")

    )||[]


    isCollected.value=

        stamps.includes(props.stamp.id)

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

<div class="stamp-card">

    

    <!-- ① 뒤쪽 : 관광지 이미지 -->
    <img
        class="stamp-photo"
        :src="image"
        alt=""
    >

    <!-- ② 앞쪽 : 카드 PNG -->
    <img
        class="card-bg"
        :src="cardImage"
        alt=""
    >

    <!-- 나머지 글씨들은 그대로 -->

    

   <!-- 가치 (리본) -->
    <div class="value">
    {{ props.stamp.weight }}
    </div>

  <!-- 도장 이미지 자리 -->
  

  <!-- 관광명소 이름 -->
    <div class="place">
    {{ stamp.place }}
    </div>

 <div class="radius">

    {{ stamp.condition.distance }}m 이내

</div>

    <!-- 날씨 -->
    <div class="weather">
        {{ stamp.special.weather }}
    </div>

    <!-- 기간 -->
    <div class="period">
        {{ stamp.special.time }}
    </div>

<div class="status">

    <span v-if="isCollected">

        ✅ 획득완료

    </span>

    <span v-else>

        🔒 미획득

    </span>

</div>

    <!-- 돋보기 버튼 (이미지 버튼 위에 투명 버튼) -->
    <button
        class="search-btn"
        @click="getLocation"
    >
    현재 위치 확인
    </button>

</div>


<!-- ===========================
        팝업
============================ -->

<div
    v-if="showPopup"
    class="popup-overlay"
    @click.self="closePopup"
>

    <div class="popup">

        <h3>{{ stamp.place }}</h3>

        <p>

            현재 거리

            {{ distance }}m

        </p>

        <template v-if="isCollected">

            <p class="success">

                ✅ 획득 완료

            </p>

        </template>

        <template v-else>

            <template v-if="canGetStamp">

                <p class="success">

                    도장 획득 가능!

                </p>

                <button @click="getStamp">

                    도장 획득하기

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

    width:380px;

    height:560px;

    position:relative;

    margin:25px;

    flex-shrink:0;

}

/* ===========================
      가치 (리본)
=========================== */

.value{

    position:absolute;

    top:28px;

    left:50%;

    transform:translateX(-50%);

    width:140px;

    text-align:center;

    font-family:neodgm_code;

    font-size:25px;

    color:white;

    z-index:2;

}

/* ===========================
      도장 이미지 자리
=========================== */

.stamp-photo{

    position:absolute;

    top:63px;

    left:50%;

    transform:translateX(-50%);

    width:220px;

    height:220px;

    object-fit:cover;

    clip-path:circle(50%);

    z-index:0;

    clip-path:circle(50%);
    object-fit:cover;

}

.stamp-image{

    width:100%;

    height:100%;

    object-fit:contain;

}

/* ===========================
      관광명소 이름
=========================== */

.place{

    position:absolute;

    top:308px;

    left:50%;

    transform:translateX(-50%);

    width:260px;

    text-align:center;

    font-family:neodgm_code;

    font-size:24px;

    color:#5A3C1C;

    z-index:2;

}

/* ===========================
   반경 / 날씨 / 기간
=========================== */

.radius{

    position:absolute;

    top:403px;

    left:47px;

    width:82px;

    line-height:18px;

    text-align:center;

    font-family:neodgm_code;

    font-size:14px;

    color:#5A3C1C;

    z-index:2;

}

.weather{

    position:absolute;

    top:403px;

    left:149px;

    width:82px;

    line-height:18px;

    text-align:center;

    font-family:neodgm_code;

    font-size:14px;

    color:#5A3C1C;

    z-index:2; 

}

.period{

    position:absolute;

    top:403px;

    left:248px;

    width:82px;

    line-height:18px;

    text-align:center;

    font-family:neodgm_code;

    font-size:14px;

    color:#5A3C1C;

    z-index:2;

}

/* ===========================
      획득 상태
=========================== */

.status{

    position:absolute;

    top:444px;

    left:50%;

    transform:translateX(-50%);

    width:260px;

    text-align:center;

    font-family:neodgm_code;

    font-size:20px;

    color:#5A3C1C;

      z-index:2;

}

/* ===========================
   현재 위치 확인 버튼
=========================== */

.search-btn{

    position:absolute;

    left:45px;

    bottom:17px;

    width:290px;

    height:58px;

    background:rgba(255,255,255,0);   /* 평소에는 완전 투명 */

    border:none;

    cursor:pointer;

    color:white;

    font-family:neodgm_code;

    font-size:20px;

    text-indent: 20px; /*글씨만 오른쪽으로 이동*/

    transition:background .18s;

    z-index:4;

}

.search-btn:hover{

    background:rgba(255,255,255,0.12);

}

.search-btn:active{

    background:rgba(255,255,255,0.20);

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


/* ===========================
      팝업 안 버튼
=========================== */

.popup button{

    width:180px;

    margin:10px auto;

    display:block;

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

    width:380px;

    height:560px;

    display:block;

    position:absolute;

    top:0;

    left:0;

    z-index:1;

}


</style>