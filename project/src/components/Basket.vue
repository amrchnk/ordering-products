<template>
<main>
  <div class="wrap text">
    <div class="wrap-in">
      <h1>Корзина</h1>
    </div>
  </div>
  <div class="wrap order-items">
    <div class="items">
      <div class="item" v-for="(product, index) in products" :key="product.id">

        <div class="image">
          <img :src=getImgUrl(product.image_name) alt="">
        </div>
        <div class="description">
          <h6>{{ product.name }}</h6>
          <h7>{{ product.category }}</h7>
          <h7>{{ product.description }}</h7>
          <div class="counter">
            <button class="btn btn-primary toogle minus" @click="counterMinus(index)">-</button>
            <label>{{ product.counter }}</label>
            <button class="btn btn-primary toogle plus" @click="counterPlus(index)">+</button>
          </div>
          <p class="price"><b>Цена:</b> {{ product.price }} руб./{{ product.unit }}</p>
          <p><b>Итого:</b> {{ product.total }} руб.</p>
        </div>

      </div>
    </div>
  </div>
  <div class="wrap total">
    <div class="total_inner">
      <div class="text">
        <h2>К оплате: {{ amount }} руб.</h2>
      </div>
      <button class="btn btn-success pay">
        <router-link to="/custdata">Заказать</router-link>
      </button>
    </div>
  </div>
</main>
</template>

<script>
export default {
  name: "Basket",
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
        total: 0,
      }],
      amount: 0,
      address: "http://localhost:5002",
      address_catalog: "http://localhost:5003", //drop later
      id_cart: null
    }
  },
  mounted() {
    this.counter
  },
  methods:{
    getImgUrl(pic) {
      return require('@/assets/' + pic);
    },
    counterPlus(index) {
      if (this.products[index].counter < this.products[index].number) {
        this.products[index].counter = this.products[index].counter + 1;
        this.products[index].total = this.products[index].counter * this.products[index].price;
      }
      else {
        alert("Максимальное количество товаров!")
      }
      this.sumAmount();
    },
    counterMinus(index) {
      if (this.products[index].counter > 0) {
        this.products[index].counter = this.products[index].counter - 1;
        this.products[index].total = this.products[index].counter * this.products[index].price;
      }
      this.sumAmount();
    },
    async getCart() {
      try {
        let id_client = Number.parseInt(document.cookie.replace(/(?:(?:^|.*;\s*)id=\s*\s*([^;]*).*$)|^.*$/, "$1"));
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
    },
    async updateProdInCart(id_prod, quantity) {
      try {
        let request = { //тело запроса на бэк
          "jsonrpc": "2.0",
          "method": "App.update_product",
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
        if (response != "success") {
          alert("Произошла ошибка, повторите операцию")
        }
      }
      catch (e) {
        console.log(e);
        alert("Сервер недоступен, попробуйте позже");
      }
    },
    async deleteProdInCart(id_prod) {
      try {
        let request = { //тело запроса на бэк
          "jsonrpc": "2.0",
          "method": "App.delete_product",
          "params": {
            "id_cart": this.id_cart,
            "id_product": id_prod
          },
          "id": 1
        }
        let response = "";
        await this.$http.post(`${this.address}/carts`, request)
          .then((res) => res.json()).then((res) => (response = res.result));
        if (response != "success") {
          alert("Произошла ошибка, повторите операцию")
        }
        this.getCart();
      }
      catch (e) {
        console.log(e);
        alert("Сервер недоступен, попробуйте позже");
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
        if (response.length === 0) {
          this.deleteCart();
        }
        else {
          let list_prod = []
          for (let i = 0; i < response.length; i++) {
            list_prod[i] = response[i].id_product;
          }
          let request = { //тело запроса на бэк
            "jsonrpc": "2.0",
            "method": "App.get_product",
            "params": { "products": list_prod },
            "id": 1
          }
          await this.$http.post(`${this.address_catalog}/catalog`, request) //по JSON RPC запросы идут только через POST
              .then((res) => res.json()).then((res) => (this.products = res.result)); //ответ берем обязательно из res.result
          for (let i = 0; i < response.length; i++) {
            let prod = this.products.find(item => item.id === response[i].id_product);
            prod.counter = response[i].quantity;
            prod.total = prod.price * prod.counter;
          }
        }
      }
      catch (e) {
        console.log(e);
        alert("Сервер недоступен, попробуйте позже");
      }
    },
    sumAmount() {
      this.amount = 0;
      for (let i = 0; i < this.products.length; i++) {
        this.amount += this.products[i].total;
      }
    },
    async deleteCart() {
      try {
        let request = { //тело запроса на бэк
          "jsonrpc": "2.0",
          "method": "App.delete_cart",
          "params": {
            "id_cart": this.id_cart
          },
          "id": 1
        }
        let response = "";
        await this.$http.post(`${this.address}/carts`, request)
          .then((res) => res.json()).then((res) => (response = res.result));
        if (response != "success") {
          alert("Произошла ошибка, повторите операцию")
        }
      }
      catch (e) {
        console.log(e);
        alert("Сервер недоступен, попробуйте позже");
      }
    },
    async updateCart() {
      try {
        let request = { //тело запроса на бэк
          "jsonrpc": "2.0",
          "method": "App.update_cart",
          "params": {
            "id_cart": this.id_cart,
            "cost": this.amount
          },
          "id": 1
        }
        let response = "";
        await this.$http.post(`${this.address}/carts`, request)
          .then((res) => res.json()).then((res) => (response = res.result));
        if (response != "success") {
          alert("Произошла ошибка, повторите операцию")
        }
      }
      catch (e) {
        console.log(e);
        alert("Сервер недоступен, попробуйте позже");
      }
    }
  },
  async created() {
    await this.getCart();
    if (this.id_cart !== null) {
      await this.getListProdOfCart();
      this.sumAmount();
    }
    else {
      alert("Ваша корзина пуста");
      this.$router.push('/catalog');
    }
  },
  async beforeDestroy() {
    if (this.id_cart !== null) {
      for (let i = 0; i < this.products.length; i++) {
        if (this.products[i].counter === 0) {
          await this.deleteProdInCart(this.products[i].id);
        }
        else {
          await this.updateProdInCart(this.products[i].id, this.products[i].counter);
        }
      }
      if (this.amount === 0) {
        await this.deleteCart();
      }
      else {
        await this.updateCart();
      }
    }
  }
}
</script>

<style scoped>
  main{
    margin-top: 60px;
  }
  h1{
    text-align: center;
    color: white;
  }
  h6{
    font-size: 1.4em;
    font-weight: bold;
    color: #184655;
  }
  .pay{
    margin:0;
    width: 120px;
  }
  h2{
    margin:0
  }
  .total_inner{
    background-color: white;
    width: 60%;
    padding: 15px 40px;
    display: flex;
    justify-content: space-between;
  }
  .total{
    margin-top: 30px;
  }
p{
  font-size: 1.1em;
  margin: 0;
}
a{
  color: white;
}
.price{
  margin-bottom: 10px;
}
  h7{
    font-size: 1em;
    color: gray;
    margin-top: 20px;
  }
  .image{
    width: 200px;
  }
  .toogle{
    width: 40px;
    text-align: center;
    margin: 0;
  }
  .item{
    padding: 30px 90px;
    display: flex;
    background-color: white;
    margin-top: 30px;
  }
  .items{
    width: 60%;
  }
  .counter{
    display: flex;
    width: 150px;
    justify-content: space-between;
    align-items: center;
    margin: 20px 0;
  }
  .description{
    margin-left: 100px;
  }
  .order-items{
    font-family: 'Open Sans', sans-serif;
  }
</style>
