module.exports = {
    root: true,
    env: {
        node: true
    },
    extends: [
        'eslint:recommended',
        'plugin:vue/vue3-essential',
        '@vue/eslint-config-typescript/recommended'
    ],
    parserOptions: {
        parser: '@typescript-eslint/parser',
        ecmaVersion: 'latest'
    },
    rules: {
        'no-unused-vars': 'off',
        '@typescript-eslint/no-unused-vars': 'warn',
        'vue/multi-word-component-names': 'off'
    }
};