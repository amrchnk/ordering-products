<template>
  <div class="modal-main">
    <div class="modal-wrap">
        <div class="modal-header">
          <h5 class="modal-title">Ошибка</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true" @click="closeModal">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <p>Упс! Кажется, возникла ошибка. Попробуйте еще раз.</p>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "payError",
  data() {
    return {
      //
    }
  },
  methods: {
    closeModal(){
      this.$emit('closeModal')
    }
  }
}

</script>

<style scoped>
	.modal-main{
		display: flex;
		height: 100%;
		justify-content: center;
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		right: 0;
		background-color: rgba(50,50,50,0.4);
	}

  .modal-wrap{
		z-index: 100;
		position: fixed;
		top: 150px;
		width: 700px;
		padding: 20px 30px;
		background-color: white;
		border-radius: 15px;
		font-family: 'Open Sans', sans-serif;
	}
</style>
