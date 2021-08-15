<template>
  <header>
    <div class="navbar">
      <router-link class="navbar-brand" to="/"><b class="header">Dostavka</b></router-link>

      <ul class="links justify-content-center">
        <li>
          <router-link class="nav-link" to="/">Главная</router-link>
        </li>
<!--        <li>-->
<!--          <router-link class="nav-link" to="/userPage" v-if="email">Главная</router-link>-->
<!--        </li>-->
        <li>
          <router-link class="nav-link" to="/catalog">Каталог</router-link>
        </li>
        <li>
          <router-link class="nav-link" to="/tracking">Отследить заказ</router-link>
        </li>
        <li>
          <router-link class="nav-link" to="/basket" v-if="email"><i class="material-icons">shopping_basket</i></router-link>
        </li>
      </ul>
      <ul class="btns" v-if="!email">
        <li>
          <router-link to="/autho" type="button" class="btn btn-outline-primary">Авторизация</router-link>
        </li>
        <li>
          <router-link to="/reg" type="button" class="btn btn-outline-primary">Регистрация</router-link>
        </li>
      </ul>

      <div class="dropdown_menu" v-if="!email">
        <div class="btn btn_dropdown medium" @click="dropDown">
          Меню
          <img v-if="!menu" class="arrow" src="@/assets/arr_down.svg" alt="">
          <img v-if="menu" class="arrow" src="@/assets/arr_up.svg" alt="">
        </div>
        <div class="btn btn_dropdown small" @click="dropDown">
          <img v-if="!menu" class="arrow" src="@/assets/menu.svg" alt="">
          <img v-if="menu" class="arrow" src="@/assets/close.svg" alt="">
        </div>
        <div class="dropdown_menu_items" v-if="menu">
          <p class="dropdown_menu_items_item autho"><router-link to="/autho" class="rl">Авторизация</router-link></p>
          <p class="dropdown_menu_items_item reg"><router-link to="/reg" class="rl">Регистрация</router-link></p>
          <p class="dropdown_menu_items_item"><router-link to="/">Главная</router-link></p>
          <p class="dropdown_menu_items_item"><router-link to="/catalog">Каталог</router-link></p>
          <p class="dropdown_menu_items_item"><router-link to="/tracking">Отследить заказ</router-link></p>
        </div>
      </div>

      <div class="dropdown_menu_user" v-if="email">
        <div class="btn btn_user" @click="dropDown">
          <div class="avatar">
            <img class="avatar" src="@/assets/ava.jpg">
          </div>
          <span>{{ this.full_name }}</span>
          <img v-if="!menu" class="arrow" src="@/assets/arr_down.svg" alt="">
          <img v-if="menu" class="arrow" src="@/assets/arr_up.svg" alt="">
        </div>

        <div class="dropdown_menu_items" v-if="menu">
          <p class="dropdown_menu_items_item m_item"><router-link to="/userPage">Главная</router-link></p>
          <p class="dropdown_menu_items_item m_item"><router-link to="/catalog">Каталог</router-link></p>
          <p class="dropdown_menu_items_item m_item"><router-link to="/tracking">Отследить заказ</router-link></p>
          <p class="dropdown_menu_items_item m_item"><router-link to="/basket">Корзина</router-link></p>
          <p class="dropdown_menu_items_item" type="button"><router-link to="/settings" class="rl">Настройки</router-link></p>
          <p class="dropdown_menu_items_item exit" type="button" @click="logout">Выйти</p>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  props: {
    cookie: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      email: "",
      full_name:"",
      menu:false
    }
  },
  watch: {
    cookie() {
      this.setEmail()
    }
  },
  mounted() {
    this.setEmail()
  },
  methods: {
    dropDown(){
      this.menu=!this.menu
    },
    setEmail() {
      this.email = this.cookie.replace(/(?:(?:^|.*;\s*)email=\s*\s*([^;]*).*$)|^.*$/, "$1");
      this.full_name=this.cookie.replace(/(?:(?:^|.*;\s*)full_name=\s*\s*([^;]*).*$)|^.*$/, "$1");
    },
    async logout() {
      //"Удаляем" куки и отправляем на страницу входа
      let cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i];
        let eqPos = cookie.indexOf("=");
        let name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
      }
      await this.$router.push('/autho');
    }
  }
}
</script>

<style scoped>

header{
  background-color: white;
  display: flex;
}

.navbar{
  display: flex;
  align-items: center;
  width: 100%;
}

ul{
  display: flex !important;
  justify-content: center !important;
  align-items: center!important;
  margin-bottom: 0;
}

li{
  list-style-type: none;
}

.header{
  color:#184655;
  font-weight:bold;
  font-size:1.3em;
  margin-left:50px;
  background-color: white;
  float: left;
}
.exit{
  color: red;
}

img{
  width: 100%;
}

.avatar{
  width: 30px !important;
  height:  30px !important;
  border-radius: 20px;
}

.btns{
  float:right;
  margin-right:50px
}

.btn{
  margin-right:10px
}

.nav-link{
  color:#4E4E4E;
  font-size:1.1em;
}

.dropdown_menu,.dropdown_menu_user{
  width: 150px;
  margin-right: 20px;
  z-index: 1000;
}
.dropdown_menu{
  display: none;
}
.btn_dropdown,.btn_user{
  width: 100%;
  text-align: left;
  color: #4E4E4E;
  font-size:1.2em!important;
  margin: 0;
  display: flex;
  justify-content: space-between;
  font-weight: 600;
}
.btn_dropdown{
  padding-right: 50px;
}
.dropdown_menu_items{
  width: 150px;
  background-color: white;
  position: absolute;
  right: 20px;
  border-radius: 5px;
  border:solid lightgray 2px;
}
.dropdown_menu_items_item{
  padding: 8px 10px;
  margin: 0;
}

.arrow{
  width: 12px;
}
.autho,.reg{
  font-weight: 600;
}
.autho{
  color: #2787F5 !important;
}
.reg{
  color: #F78306 !important;
}
.rl{
  text-decoration: none;
  color: inherit!important;
}

.small{
  display: none;
}
.m_item{
  display: none;
}
@media (max-width: 1040px){
  .header{
    font-size: 1.1em;
    margin-left: 20px;
  }

  .nav-link{
    font-size:1em;
  }

  .btn{
    font-size: 0.9em;
  }

  .btns{
    float:right;
    margin-right:20px
  }
}

@media (max-width: 810px){
  ul{
    display: none!important;
  }
  .m_item{
    display: block;
  }
  .dropdown_menu{
    display: block;
  }
}
@media (max-width: 630px){
  .medium{
    display: none;
  }
  .small{
    display: block;
  }
  .arrow{
    width: 20px;
  }
  .btn_dropdown{
    text-align: right;
    padding-right: 0;
  }
  .dropdown_menu{
    width: 40px;
  }
  .dropdown_menu_items{
    width: 100%;
    background-color: white;
    position: absolute;
    right: 0;
    top: 59px;
    border-radius:0;
    border:none;
  }
  .dropdown_menu_items_item{
    padding: 8px 10px;
    margin: 0;
    margin-left: 10px;
  }
}
@media (max-width: 375px){
  .dropdown_menu_user{
    margin-right: 12px;
  }
}
</style>
