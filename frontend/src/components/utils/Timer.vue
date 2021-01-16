<template>
    <div class="text-center">
    <p class="text-black text-sm" v-if="currentTime">
      {{
        currentTime
          ? `You need to wait ${("0" + currentTime.seconds).slice(-2)} seconds`
          : ""
      }}
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