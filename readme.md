# Selenium Testing with CrossBrowserTesting and Behave

[Behavior Driver Development](https://en.wikipedia.org/wiki/Behavior-driven_development) is growing in popularity, and performing BDD with Python is no exception. [Behave](http://pythonhosted.org/behave/) is a popular BDD framework for performing tests, and, because Behave is built on Python's Selenium language bindings, performing Behavioural Driven testing on CBT is easy. We'll walk your through getting started here.

To get started, we'll need to ensure that Behave is installed. The easiest means of doing so is with Pip:

```
pip install Behave
```

Alternatively you can read [installation documenation](http://pythonhosted.org/behave/install.html) on the Behave website. Once that's complete, we're ready to start writing our first test with Behave.

Tests start with writing "Feature" files that use plain english to describe the steps of your test. Features use keywords to form the actual steps being taken in the test:

* **Given** we put the system in a known state before the user (or external system) starts interacting with the system (in the When steps). Avoid talking about user interaction in givens.

* **When** we take key actions the user (or external system) performs. This is the interaction with your system which should (or perhaps should not) cause some state to change.

* **Then** we observe outcomes.