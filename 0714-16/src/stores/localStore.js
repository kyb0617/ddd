import { defineStore } from "pinia"


export const useLocalStore =
defineStore("local", {


state:()=>({

    stamps:[]

}),


actions:{


async loadStamps(){

    const res =
    await fetch("/data/stamps.json")

    this.stamps =
    await res.json()

}


}


})