<script setup>

import {ref, onMounted, computed} from "vue"

import {useLocalStore}
from "./stores/localStore"

import StampCard
from "./components/StampCard.vue"


const store =
useLocalStore()

const refresh = ref(0)

onMounted(()=>{

store.loadStamps()

})

const totalPoint = computed(()=>{

refresh.value

let myStamps =
JSON.parse(
localStorage.getItem("myStamps")
)
|| []


return store.stamps

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
LocalHub 도장 도감
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

<div class="stamp-list">


<StampCard

v-for="stamp in store.stamps"

:key="stamp.id"

:stamp="stamp"

/>

</div>


</template>

<style>

.stamp-list {

display:flex;

flex-wrap:wrap;

gap:20px;

justify-content:flex-start;

}

.top-bar{

display:flex;

justify-content:space-between;

align-items:center;

margin-bottom:30px;

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