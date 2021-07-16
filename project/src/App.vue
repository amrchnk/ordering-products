<template>
  <div id="app">
    <Header :cookie="cookie"/>
    <router-view/>
  </div>
</template>
<script>
import Header from '@/components/Header'
export default {
  name: 'App',
  components: {
   Header
  },
  data() {
    return {
      cookie: document.cookie
    }
  },
  beforeUpdate() {
    this.cookie = document.cookie
  }
}
</script>

<style>
body,html{
  height: 100%;
}
#app{
  font-family: 'Raleway', sans-serif;
  font-feature-settings: 'lnum' 1;
  display: flex;
  flex-direction: column;
  height: 100%;
}

body{
  background-color: #FFDE40;
}
</style>



