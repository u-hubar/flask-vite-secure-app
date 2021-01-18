<template>
    <div class="text-center">
    <p class="text-black text-sm" v-if="currentTime" v-text="message">
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, watch, computed } from "vue";
export default defineComponent({
  props: {
    deadline: {
      type: Number,
      required: true
    },
    speed: {
      type: Number,
      default: 1000
    }
  },
  data() {
    return {
      currentTime: null
    };
  },
  mounted() {
    setTimeout(this.countdown, 1);
  },
  emits: ['reset'],
  computed: {
    message() {
      const { minutes, seconds } = this.currentTime;
      let text = "You need to wait ";
      if (minutes) text += `${minutes} minutes`
      if (minutes && seconds) text += ' and '
      if (seconds) text += `${seconds} seconds`

      return this.currentTime ? text : '';
    }
  },
  methods: {
    countdown() {
      let t = this.deadline - Date.parse(new Date().toString());
      let seconds = Math.floor((t / 1000) % 60);
      let minutes = Math.floor((t / 1000 / 60) % 60);
      let hours = Math.floor((t / (1000 * 60 * 60)) % 24);
      let days = Math.floor(t / (1000 * 60 * 60 * 24));
      if (t > 0) {
        this.currentTime = {
          total: t,
          days: days,
          hours: hours,
          minutes: minutes,
          seconds: seconds
        };
        setTimeout(this.countdown, this.speed);
      } else {
        this.currentTime = null;
      }
    }
  },
  watch: {
    currentTime(value) {
      if (!value) this.$emit('reset', true)
    }
  }
})

</script>