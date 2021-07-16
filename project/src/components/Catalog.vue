<template>
<main>
  <div class="wrap text">
    <h1>Каталог товаров</h1>
  </div>
  <div class="wrap">
    <div class="select-wrap">
      <select name="" id="" class="form-select" @change="onchange()"  v-model="key">
        <option disabled>Фильтр по:</option>
        <option :value="filter" v-for="filter in filters">{{filter}}</option>
      </select>
    </div>
  </div>

  <div class="wrap">
    <div class="catalog">
      <div class="str">
        <div class="item" v-for="(product, index) in products" :key="product.id">
          <div class="image">
            <img :src=getImgUrl(product.image_name) alt="">
          </div>
          <div class="description">
            <h3>{{ product.name }}</h3>
            <h4>{{ product.category }}</h4>
            <p>{{ product.description }}</p>
            <h4>Цена:<span class="price">{{ product.price }}</span> руб./{{ product.unit }}</h4>
          </div>
          <div class="counter">
            <button class="btn btn-primary toogle minus" @click="counterMinus(index)" :disabled="product.added">-</button>
            <label>{{ product.counter }}</label>
            <button class="btn btn-primary toogle plus" @click="counterPlus(index)" :disabled="product.added">+</button>
          </div>
          <div v-if="product.added">
            <span>Добавлено</span>
          </div>
          <div v-else>
            <button class="btn btn-success pay" @click="addInCart(product.id, product.counter, index)">
              В корзину
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</main>
</template>

<script>
export default {
name: "Catalog",
  data() {
    return {
      products:[{
        id:'',
        name: "",
        category: "",
        description: '',
        image_name: '',
        unit: '',
        price: 0,
        number: 0,
        counter: 0,
        added: false
      }],
      filters:[],
      filter: "Все",
      selected:'',//значение менять по фильтру, значения должны быть ТОЧНО как категории в бд
      address: "http://localhost:5002",
      address_catalog: "http://localhost:5003", //drop later
      id_cart: null
    }
  },
  mounted() {

  },
  methods:{
    getImgUrl(pic) {
      return require('@/assets/' + pic);
    },
    counterPlus(index){
      if(this.products[index].counter<this.products[index].number){
        this.products[index].counter=this.products[index].counter+1;
      }
    },
    counterMinus(index){
      if(this.products[index].counter>0){
        this.products[index].counter=this.products[index].counter-1;
      }
    },
    async getProducts(){
      try {
        let request = { //тело запроса на бэк
          "jsonrpc": "2.0",
          "method": "App.get_catalog",
          "params": { "filter": this.filter },
          "id": 1
        }
        await this.$http.post(`${this.address_catalog}/catalog`, request) //по JSON RPC запросы идут только через POST
            .then((res) => res.json()).then((res) => (this.products = res.result)); //ответ берем обязательно из res.result
        if (this.products === -1 || this.products === null) { //убрать блок? или как-то переписать, потому что в этом случае с бэка приходит []
          alert("Произошла ошибка, повторите вход");
        } else if (this.products.length === 0){
          alert("Продуктов нет");
        }
      } catch (e) {
        console.log(e);
        alert("Сервер недоступен, попробуйте позже");
      }
    },
    async getFilters(){
      try {
        let request = { //тело запроса на бэк
          "jsonrpc": "2.0",
          "method": "App.get_filters",
          "params": { },
          "id": 1
        }
        await this.$http.post(`${this.address_catalog}/catalog`, request) //по JSON RPC запросы идут только через POST
            .then((res) => res.json()).then((res) => (this.filters = res.result)); //ответ берем обязательно из res.result
        if (this.filters === -1 || this.filters === null) { //убрать блок? или как-то переписать, потому что в этом случае с бэка приходит []
          alert("Произошла ошибка, повторите вход");
        } else if (this.filters.length === 0){
          alert("Фильтров нет");
        }
      } catch (e) {
        console.log(e);
        alert("Сервер недоступен, попробуйте позже");
      }
    },
    onchange() {
      this.filter=this.key;
      this.getProducts();
    },
    async addInCart(id_prod, quantity, index) {
      try {
        let id_client = Number.parseInt(document.cookie.replace(/(?:(?:^|.*;\s*)id=\s*\s*([^;]*).*$)|^.*$/, "$1"));
        if (isNaN(id_client) !== true) { //проверяем, залогинен ли клиент
          if (this.id_cart === null) { //если корзины еще нет, создаем ее
            await this.addNewCart();
          }
          let request = { //тело запроса на бэк
            "jsonrpc": "2.0",
            "method": "App.add_product",
            "params": {
              "id_cart": this.id_cart,
              "id_product": id_prod,
              "quantity": quantity
            },
            "id": 1
          }
          let response = "";
          await this.$http.post(`${this.address}/carts`, request)
            .then((res) => res.json()).then((res) => (response = res.result));
          if (response !== "success") {
            alert("Произошла ошибка, повторите операцию")
          }
          else {
            this.products[index].added = true
          }
        }
        else {
          alert('Чтобы добавить товар в корзину, вам необходимо зарегистрироваться')
          this.$router.push('/autho');
        }
      }
      catch (e) {
        console.log(e);
        alert("Сервер недоступен, попробуйте позже");
      }
    },
    async getCart() {
      let id_client = Number.parseInt(document.cookie.replace(/(?:(?:^|.*;\s*)id=\s*\s*([^;]*).*$)|^.*$/, "$1"));
      if(isNaN(id_client)!==true){
        try {
          let request = {
            "jsonrpc": "2.0",
            "method": "App.get_cart",
            "params": {
              "id_client": id_client //брать из куки
            },
            "id": 1
          }
          let response = "";
          await this.$http.post(`${this.address}/carts`, request)
              .then((res) => res.json()).then((res) => (response = res.result));
          if (response['error'] == '') {
            this.id_cart = response['id']
          }
        }
        catch (e) {
          console.log(e)
          alert("Сервер недоступен, попробуйте позже");
        }
      }
    },
    async getListProdOfCart() {
      try {
        let request = { //тело запроса на бэк
          "jsonrpc": "2.0",
          "method": "App.get_list_prod",
          "params": {
            "id_cart": this.id_cart
          },
          "id": 1
        }
        let response = [];
        await this.$http.post(`${this.address}/carts`, request)
          .then((res) => res.json()).then((res) => (response = res.result));
        if (response.length !== 0) {
          for (let i = 0; i < response.length; i++) {
            let prod = this.products.find(item => item.id === response[i].id_product);
            prod.added = true;
            prod.counter = response[i].quantity;
          }
        }
      }
      catch (e) {
        console.log(e);
        alert("Сервер недоступен, попробуйте позже");
      }
    },
    async addNewCart() {
      try {
        let id_client = Number.parseInt(document.cookie.replace(/(?:(?:^|.*;\s*)id=\s*\s*([^;]*).*$)|^.*$/, "$1"));
        let request = { //тело запроса на бэк
          "jsonrpc": "2.0",
          "method": "App.add_cart",
          "params": {"id_client": id_client}, //брать id клиента из куки
          "id": 1
        }
        await this.$http.post(`${this.address}/carts`, request)
          .then((res) => res.json()).then((res) => (this.id_cart = Number.parseInt(res.result)));
      }
      catch (e) {
        console.log(e);
        alert("Сервер недоступен, попробуйте позже");
      }
    }
  },
  async created() {
    await this.getProducts();
    await this.getFilters();
    await this.getCart();
    if (this.id_cart !== null) {
      await this.getListProdOfCart()
    }
  }
}
</script>

<style scoped>
.str{
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  margin-top: 10px;
  width: 100%;
}
.select-wrap{
  width: 60%;
  display: flex;
  align-items: flex-start;
}
.catalog{
  width: 60%;
  display:flex;
  justify-content: space-between;
}
h1{
  text-align: left;
}
select{
  width: 200px;
  margin-top: 20px;
}
.item{
  background-color: white;
  max-width: 32%;
  border-radius: 20px;
  padding: 30px 40px;
  margin-top: 20px;
  /*margin-right: 15px;*/
}

.text{
  margin-top: 30px;
  width: 60%;
  text-align: left;
}
a{
  color: white;
}
img{
  width: 60%;
}
.price{
  font-family: 'Open Sans', sans-serif;
}
.toogle{
  width: 40px;
  text-align: center;
  margin: 0;
}
.counter{
  display: flex;
  width: 150px;
  justify-content: space-between;
  align-items: center;
  margin: 20px 0;
}
.image{
  display: flex;
  width: 100%;
  justify-content: center;
}
label{
  font-family: 'Open Sans', sans-serif;
}
h3{
  margin-top: 15px;
}
.pay{
  margin:0;
  width: 100%;
}
</style>
