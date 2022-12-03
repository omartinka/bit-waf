<template>
  <div class="container">
    Application: {{ host }}

    <div v-for="e of endpoints">
      <Endpoint :ref="e" :path="e"/>
    </div>

    <div class="add_endpoint">
      Endpoint:
      <input v-model="path" type="text">
      <button @click="add_path()">Add endpoint</button>
    </div>
  </div>
</template>

<script>
import Endpoint from './Endpoint.vue';

export default {
  name: "Container",
  props: {
    host: ""
  },
  data() {
    return {
      path: "",
      endpoints: []
    }
  },
  components: {
    Endpoint
  },
  methods: {
    add_path() {
      this.endpoints.push(this.path);
    },
    get_config() {
      let arr= []
      for (let ep of this.endpoints) {
        arr.push( this.$refs[ep][0].get_config())
      }
      return arr;
    }
  }
}
</script>

<style>
.container {
  outline: 1px solid black;
  padding: 5px;
  margin: 10px;
}
.add_endpoint {
  padding: 5px;
  margin: 10px;
  outline: 1px solid black;
}
</style>