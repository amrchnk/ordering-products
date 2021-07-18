<template>
<main>
  <div class="wrap">
    <div class="text">
      <h1>Каталог товаров</h1>
    </div>
  </div>

  <div class="wrap">
    <div class="select">
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
          <div class="first">
            <div class="image">
              <img :src=getImgUrl(product.image_name) alt="">
            </div>
            <div class="description">
              <h3>{{ product.name }}</h3>
              <span class="category">{{ product.category }}</span>
              <p class="description">{{ product.description }}</p>
            </div>
          </div>
          <div class="second">
            <h4><span class="price">{{ product.price }}</span> руб./{{ product.unit }}</h4>
            <div class="counter">
              <button class="btn btn-primary toogle minus" @click="counterMinus(index)" :disabled="product.added"><img
                  src="@/assets/minus.svg" alt=""></button>
              <label>{{ product.counter }}</label>
              <button class="btn btn-primary toogle plus" @click="counterPlus(index)" :disabled="product.added"><img
                  src="@/assets/plus.svg" alt=""></button>
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

main{
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
}

.wrap{
  width: 70%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.text{
  width: 100%;
  margin-top: 50px;
}
h1{
  font-size: 3.4em;
  font-weight: bold;
}

.select{
  width: 100%;
  display: flex;
  justify-content: flex-start;
  margin-top: 25px;
}

select{
  width: 12em;
}

.catalog{
  width: 100%;
  display:flex;
  justify-content: space-between;
  margin: 0 -15px 0 0;
}

.str{
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  margin-top: 10px;
  width: 100%;
}

.item{
  background-color: white;
  width: 23%;
  margin-right: 15px;
  border-radius: 20px;
  padding: 30px 25px;
  margin-top: 15px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.image{
  display: flex;
  width: 100%;
  justify-content: center;
}

label,.price{
  font-family: 'Open Sans', sans-serif;
}

.toogle{
   width: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
   margin: 0;
 }

.counter{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 15px 0 5px;
}

h3{
  font-size: 1.6em;
  margin: 15px 0;
}
.pay{
  margin-top:15px;
  width: 100%;
}

.category{
  background-color: #5B5B5E;
  color: white;
  border-radius: 10px;
  margin: 10px 0;
  padding: 6px 10px;
}

.description{
  margin: 10px 0;
}

@media (max-width: 1350px){
  h3{
    font-size: 1.3em;
    margin: 15px 0 10px;
  }
  .description{
    font-size: 0.9em;
  }
  .category{
    font-size: 0.8em;
  }
  h4{
    font-size: 1em;
  }
  h1{
    font-size: 3em;
  }
  .select{
    margin-top: 15px;
  }

  img{
    width: 100%;

  }
  .toogle{
    width: 2.1em;
    height: 2.1em;
  }
  .pay{
    margin-top:10px;
    width: 100%;
    font-size: 0.9em;
  }
  label{
    font-size: 0.9em;
  }
}

@media (max-width: 1200px){
  .item{
    padding: 20px;
  }
}

@media (max-width: 1070px){
  .item{
    width: 30%;

  }
}
@media (max-width: 1000px){
  h1{
    font-size: 2.5em;
  }
}
@media (max-width: 520px){
  h1{
    font-size: 2em;
  }
}

@media (max-width: 375px){
  h1{
    font-size: 1.9em;
  }
}
</style>
