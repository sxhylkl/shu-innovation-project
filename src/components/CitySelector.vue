<template>
    <el-cascader
    v-model="value"
    :options="cities"
    :show-all-levels="showAllLevels"
    :filterable="filterable"
    @change="$emit('change')"
    ></el-cascader>
</template>

<script>
import cities from './cities.json'

export default {
    props: {
        filterable: {
            type: Boolean,
            default: false
        },
        showAllLevels: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            cities,
            value: ''
        }
    }
}
</script>

<style lang="scss" scoped>

</style>
