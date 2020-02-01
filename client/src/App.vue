<template>
  <div id="app">
    <div>
      <b-navbar toggleable="lg" type="dark" variant="info">
        <b-navbar-brand href="#">AC Manager</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse id="nav-collapse" is-nav>

          <b-navbar-nav class="ml-auto">
            <b-button v-if="!user" @click="onSignIn">Sign In</b-button>
            <b-nav-text v-if="user">{{user.getName()}}</b-nav-text>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
    <router-view/>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      user: undefined
    }
  },
  methods: {
    async onSignIn() {
      window.location.replace("api/login")
    }
  }
}
</script>

<style>

</style>
