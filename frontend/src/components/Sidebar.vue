<template>
  <div class="flex">
    <!-- Backdrop -->
    <div
      :class="isOpen ? 'block' : 'hidden'"
      @click="isOpen = false"
      class="fixed z-20 inset-0 bg-black opacity-50 transition-opacity lg:hidden"
    ></div>
    <!-- End Backdrop -->

    <div
      :class="isOpen ? 'translate-x-0 ease-out' : '-translate-x-full ease-in'"
      class="fixed z-30 inset-y-0 left-0 w-64 transition duration-300 transform bg-gray-900 overflow-y-auto lg:translate-x-0 lg:static lg:inset-0"
    >
      <div class="text-center mt-8">
          <span class="text-white text-2xl mx-2 font-semibold"
            >Password Manager</span
          >
      </div>

      <nav class="mt-10">
        

        <router-link
          class="flex items-center duration-200 mt-4 py-2 px-6 border-l-4"
          :class="[$route.name === 'Dashboard' ? activeClass : inactiveClass]"
          to="/dashboard"
        >
           <svg class="h-5 w-5"
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
           >
								<path
              d="M7 3C6.44772 3 6 3.44772 6 4C6 4.55228 6.44772 5 7 5H13C13.5523 5 14 4.55228 14 4C14 3.44772 13.5523 3 13 3H7Z"
              fill="currentColor"
            />
            <path
              d="M4 7C4 6.44772 4.44772 6 5 6H15C15.5523 6 16 6.44772 16 7C16 7.55228 15.5523 8 15 8H5C4.44772 8 4 7.55228 4 7Z"
              fill="currentColor"
            />
            <path
              d="M2 11C2 9.89543 2.89543 9 4 9H16C17.1046 9 18 9.89543 18 11V15C18 16.1046 17.1046 17 16 17H4C2.89543 17 2 16.1046 2 15V11Z"
              fill="currentColor"
            />
							</svg>

          <span class="mx-4">My Items</span>
        </router-link>


        <router-link
          class="flex items-center duration-200 mt-4 py-2 px-6 border-l-4"
          :class="[$route.name === 'Blank' ? activeClass : inactiveClass]"
          to="/logs"
        >
          <svg fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" stroke="currentColor" class="h-5 w-5">
								<path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
								<path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
							</svg>

          <span class="mx-4">Logs</span>
        </router-link>
        
        <router-link
          class="flex items-center duration-200 mt-4 py-2 px-6 border-l-4 text-gray-300  hover:text-red-500"
          :class="[$route.name === 'Login' ? activeClass : inactiveClass]"
          to="/"
        >
          <svg class="fill-current h-5 w-5 " viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M13 4.00894C13.0002 3.45665 12.5527 3.00876 12.0004 3.00854C11.4481 3.00833 11.0002 3.45587 11 4.00815L10.9968 12.0116C10.9966 12.5639 11.4442 13.0118 11.9965 13.012C12.5487 13.0122 12.9966 12.5647 12.9968 12.0124L13 4.00894Z" fill="currentColor"></path>
                <path d="M4 12.9917C4 10.7826 4.89541 8.7826 6.34308 7.33488L7.7573 8.7491C6.67155 9.83488 6 11.3349 6 12.9917C6 16.3054 8.68629 18.9917 12 18.9917C15.3137 18.9917 18 16.3054 18 12.9917C18 11.3348 17.3284 9.83482 16.2426 8.74903L17.6568 7.33481C19.1046 8.78253 20 10.7825 20 12.9917C20 17.41 16.4183 20.9917 12 20.9917C7.58172 20.9917 4 17.41 4 12.9917Z" fill="currentColor"></path>
              </svg>

          <span @click="resetTokens()" class="mx-4">Logout</span>
        </router-link>
      </nav>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useSidebar } from "../hooks/useSidebar";
import { resetTokens } from "../hooks/useSession";

export default defineComponent({
  setup() {
    const { isOpen } = useSidebar();
    const activeClass = ref(
      "bg-gray-600 bg-opacity-25 text-gray-100 border-gray-100"
    );
    const inactiveClass = ref(
      "border-gray-900 text-gray-400 hover:bg-gray-600 hover:bg-opacity-25 hover:text-gray-100"
    );

    return {
      isOpen,
      activeClass,
      inactiveClass,
      resetTokens
    };
  },
});
</script>
