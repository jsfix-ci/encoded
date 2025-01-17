@cart
Feature: Cart
    Scenario: Search result cart toggles:
        When I visit "/search/?type=Experiment&control_type!=*&status=released&perturbed=false"
        And I wait for the content to load
        Then I should see 25 elements with the css selector ".result-item__cart-control"

        When I press "/experiments/ENCSR611ZAL/"
        And I wait for 3 seconds
        And I press "/experiments/ENCSR000INT/"
        And I wait for 3 seconds
        And I press "/experiments/ENCSR000DZQ/"
        And I wait for 3 seconds
        Then I should see 3 elements with the css selector ".cart-toggle--in-cart"
        And I should see an element with the css selector ".cart__nav-button"

        When I visit "/search/?type=FunctionalCharacterizationExperiment&type=FunctionalCharacterizationSeries&config=FunctionalCharacterization&datapoint=false&control_type!=*"
        And I wait for the content to load
        Then I should see 6 elements with the css selector ".result-item__cart-control"

        When I press "Add all items to cart"
        Then I should see 6 elements with the css selector ".cart-toggle--in-cart"

        When I visit "/search/?type=FunctionalCharacterizationExperiment&accession=ENCSR127PCE"
        And I wait for the content to load
        Then I should see 1 elements with the css selector ".result-item__cart-control"

        When I press "/functional-characterization-experiments/ENCSR127PCE/"
        And I wait for 3 seconds
        Then I should see 1 elements with the css selector ".cart-toggle--in-cart"

    Scenario: Cart page load
        When I press "cart-control"
        And I click the link to "/cart-view/"
        And I wait for the content to load
        Then I should see 11 elements with the css selector ".result-item"
        When I press "cart-facet-term-hg19"
        Then I should see "6 files selected"
        When I press "cart-facet-term-Experiment"
        Then I should see "3 files selected"

    Scenario: Exercise file facets
        When I click the link to "#processeddata"
        Then I should see 3 elements with the css selector ".cart-list-item"
        When I press "default-data-toggle"
        Then I should see "3 files selected"
        And I should see 3 elements with the css selector ".cart-list-item"
        When I click the link to "#rawdata"
        Then I should see 0 elements with the css selector ".cart-list-item"

    Scenario: Cart page interactions
        When I click the link to "#processeddata"
        And I press "More filters"
        And I press "output_type-label"
        And I press "cart-facet-term-IDR ranked peaks"
        And I press "close-modal"
        Then I should see "1 file selected"
        And I should see 1 elements with the css selector ".cart-list-item"
        When I press "More filters"
        And I press "cart-facet-clear-output_type"
        And I press "close-modal"
        Then I should see "3 files selected"
        And I should see 3 elements with the css selector ".cart-list-item"
        When I press "Download"
        Then I should see an element with the css selector ".modal"
        When I press "Close"
        Then I should not see an element with the css selector ".modal"
        When I click the link to "#datasets"
        And I wait for 5 seconds
        And I press "/experiments/ENCSR000INT/"
        And I wait for the content to load
        And I press "cart-facet-term-GRCh38"
        Then I should see 10 elements with the css selector ".result-item"
        And I should see "5 files selected"

    Scenario: Cart description
        When I press "edit-description"
        Then I should see an element with id "description-editor"
        And I should see an element with id "text-editing-area"
        When I press "Close without saving"
        Then I should not see an element with id "description-editor"

    Scenario: Cart listing
        When I press "List cart"
        Then I should see an element with id "description-editor"
        When I fill in "cart-description-text-area" with "This is a description."
        And I press "Save description"
        And I press "Close"
        Then I should not see an element with id "description-editor"
        And I should see "This is a description."

    Scenario: Clearing the cart 
        When I press "clear-cart-actuator"
        Then I should see an element with the css selector ".modal"
        When I press "clear-cart-submit"
        Then I should not see an element with the css selector ".modal"
        And I should see "Empty cart"
