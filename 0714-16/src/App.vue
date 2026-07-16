<script setup>

import {ref, onMounted, computed} from "vue"

function horizontalScroll(event){

    const list = event.currentTarget

    if(event.deltaY !== 0){

        event.preventDefault()

        list.scrollLeft += event.deltaY

    }

}

import {useLocalStore}
from "./stores/localStore"

import StampCard from "./components/StampCard.vue"
import rarityBar from "./assets/images/raritybar.png"

const placeImages = Object.values(
  import.meta.glob(
    '@/assets/images/place/*.png',
    {
      eager: true,
      query: '?url',
      import: 'default'
    }
  )
)

const store =
useLocalStore()

const refresh = ref(0)

const stamps = ref([])

onMounted(async()=>{

    const response = await fetch("/data/stamps.json")

    const data = await response.json()

    console.log(data)

    stamps.value = data

})
const totalPoint = computed(()=>{

refresh.value

let myStamps =
JSON.parse(
localStorage.getItem("myStamps")
)
|| []


return stamps.value

.filter(
(stamp)=>
myStamps.includes(stamp.id)
)

.reduce(
(sum,stamp)=>
sum + stamp.weight,
0
)


})

function resetStamps(){

localStorage.removeItem("myStamps")

location.reload()

}

window.addEventListener(
"stampUpdated",
()=>{

refresh.value++

}
)

</script>


<template>

<div class="top-bar">

<h1>
도장 도감
</h1>


<div class="user-menu">

<button>
💎 {{ totalPoint }}
</button>


<button @click="resetStamps">
🔄 리셋
</button>

</div>

</div>

<img
class="rarity-bar"
:src="rarityBar"
/>

<div
    class="stamp-list"
    @wheel="horizontalScroll"
 >


<StampCard
  v-for="(stamp, index) in stamps"
  :key="stamp.id"
  :stamp="stamp"
  :image="placeImages[index]"
/>

/>

</div>

</template>

<style>

.rarity-bar{

    display:block;

    width:720px;

    max-width:40%;

    margin:5px auto 0px;

    border:2px slid red;

}

.stamp-list{

    display:flex;

    flex-direction:row;

    flex-wrap:nowrap;   /* 줄바꿈 금지 */

    gap:20px;

    justify-content:flex-start;

    align-items:flex-start;

    overflow-x:auto;    /* 가로 스크롤 */

    overflow-y:hidden;

    width:100vw;

    padding:20px;

}
.stamp-card{

width:380px;

position:relative;

flex:0 0 380px;   /* 카드 크기 고정 */

margin:25px auto;

}

.top-bar{

display:flex;

justify-content:space-between;

align-items:center;

margin-bottom:5px;

}


.user-menu{

display:flex;

gap:10px;

}


.user-menu button{

padding:10px 15px;

border-radius:10px;

border:none;

background:#8b4513;

color:white;

font-size:16px;

cursor:pointer;

}


.user-menu button:hover{

opacity:0.8;

}

</style>