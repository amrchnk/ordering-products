<template>
<main>
  <div class="wrap">
    <div class="text">
      <h1>Корзина</h1>
    </div>
  </div>
  <div class="wrap">
    <div class="container">
      <div class="left_wrap">
        <div class="left">
          <div class="total">
            <h2>Итого</h2>
            <hr>
          </div>
          <h3>К оплате: <span class="num">{{ amount }}</span> руб.</h3>
          <button class="btn btn-success pay">
            <router-link to="/custdata">Оплатить</router-link>
          </button>
        </div>
      </div>

      <div class="items">
        <div class="item_wrap" v-for="(product, index) in products" :key="product.id">
          <div class="item">
            <div class="image">
              <img :src=getImgUrl(product.image_name) alt="">
            </div>
            <div class="description">
              <h6>{{ product.name }}</h6>
              <span class="category">{{ product.category }}</span>
              <h7>{{ product.description }}</h7>
              <div class="counter">
                <button class="btn btn-primary toogle minus" @click="counterMinus(index)">
                  <img class="b_img" src="@/assets/minus.svg" alt="">
                </button>
                <label class="num">{{ product.counter }}</label>
                <button class="btn btn-primary toogle plus" @click="counterPlus(index)">
                  <img class="b_img" src="@/assets/plus.svg" alt="">
                </button>
              </div>
              <p class="price"><b>Цена:</b> <span class="num">{{ product.price }}</span> руб./{{ product.unit }}</p>
              <p class="price"><b>Итого:</b> <span class="num">{{ product.total }}</span> руб.</p>
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
  color: white;
}

.container{
  display: flex;
  width: 100%;
  padding: 0;
  margin-top: 20px;
}

.item,.left{
  background-color: white;
  border-radius: 10px;
}
.left_wrap{
  width: 35%;
}
.items{
  width: 65%;
}
.left{
  margin-right: 15px;
  padding: 20px;
}
.item{
  display: flex;
  margin-bottom: 15px;
  padding: 15px;
}
.image{
  width: 30%;
  padding: 10px;
}
.description{
  padding: 10px;
}
h6{
  font-size: 1.5em;
  font-weight: bold;
  color: #184655;
}
.category{
  background-color: #FFFDC5;
  color: #5B5B5E;
  border-radius: 10px;
  margin: 10px 0;
  padding: 4px 10px;
  font-size: 0.9em;
}

.counter{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20px 0;
}
.toogle{
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 12px;
}
.b_img{
  width: 100%;
}
.num{
  font-family: 'Open Sans', sans-serif;
}
p{
  margin-bottom: 10px;
}
.price{
  font-size: 1.2em;
}

h2{
  font-weight: 400;
}
h3{
  margin: 15px 0;
}
a{
  text-decoration: none;
  color: inherit;
}
.pay{
  color: white;
  font-size: 1.2em;
  margin-top: 5px;
}
img{
  width: 100%;
}

@media (max-width: 1700px){
  .image{
    width: 40%;
  }
}

@media (max-width: 1350px) {
  h1 {
    font-size: 3em;
  }
  .image{
    width: 45%;
  }
  h2{
    font-size: 1.8em;
  }
}

@media (max-width: 1100px) {
  h1 {
    font-size: 2.5em;
  }
  h2{
    font-size: 1.5em;
  }
  h3{
    font-size: 1.2em;
    margin: 12px 0;
  }
  h6{
    font-size: 1.4em;
  }
  .toogle{
    width: 1.8em;
    height: 1.8em;
    padding: 8px;
  }
  .price{
    font-size: 1em;
  }
  p{
    margin-bottom: 5px;
  }
  .category{
    margin: 5px 0;
    padding: 4px 8px;
    font-size: 0.8em;
  }
  .counter{
    margin: 10px 0;
  }
  .pay{
    font-size: 1em;
    padding: 5px 10px;
  }
}

@media (max-width: 980px) {
  .container{
    flex-direction: column-reverse;
  }
  .left_wrap,.items{
    width: 100%;
  }
  .left{
    margin: 0;
  }
  .image{
    width: 35%;
  }
}

@media (max-width: 800px){
  .image{
    width: 43%;
  }
}

@media (max-width: 600px) {
  h1 {
    font-size: 2.3em;
  }
  .image{
    width: 50%;
  }

}
@media (max-width: 490px) {
  .wrap {
    width: 80%;
  }
  h2{
    font-size: 1.3em;
  }
  h3{
    font-size: 1.2em;
    margin: 10px 0;
  }
  h6{
    font-size: 1em;
  }
  .price{
    font-size: 0.8em;
  }
  label{
    font-size: 0.8em;
  }
  .toogle{
    width: 1.6em;
    height: 1.6em;
    padding: 8px;
  }
  .description{
    padding: 10px 0;
  }
}
@media (max-width: 390px) {
  h1 {
    font-size: 1.8em;
  }
  h2{
    font-size: 1.1em;
  }
  h3{
    font-size: 1em;
    margin: 8px 0;
  }
}


</style>
