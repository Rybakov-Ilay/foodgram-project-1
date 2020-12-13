class IngredientValue {
    constructor(config, api) {
        this.config = config;
        this.api = api;
    }

    removeSubscribe(target, ingredientValue_id) {
        target.setAttribute('disabled', true)
        this.api.removeIngredientValue(ingredientValue_id)
            .then(e => {
                target.innerHTML = this.config.default.text;
                target.classList.add(this.config.default.class);
                target.classList.remove(this.config.active.class);
                target.setAttribute(this.config.attr, true);
            })
            .catch(e => {
                console.log(e)
            })
            .finally(e => {
                target.removeAttribute('disabled');
            })
    };
}