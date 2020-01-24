# Volta design system

This is Volta, the design system for Vonage. If you just want to use the design system on your project, you can go to http://volta.vonage.com (vonage/vonage) and download the package.

Contents:
- [For users](#forusers)
- [For contributors](#forcontributors)

# For users

## Quick start

- Add the package to your project 
- Call `volta.css` (or volta.min.css) and `volta.js` (or volta.min.js) in all your files (plus `volta.templates.css` or volta.templates.min.css if you're using our templates)
- Refer to the [documentation](http://volta.vonage.com) (user: vonage, password: vonage) to write your markup correctly so that the styles will be applied
- Make a not of the location of your `symbol` folder, as it contains the compiled icon file

This is how your header might look like

```html
<link rel="stylesheet" href="path-to-volta/dist/css/volta.css"/>

<script type="text/javascript" src="path-to-volta/dist/js/volta.js"></script>
<!-- The next two files are needed just for tooltips - read more below -->
<script type="text/javascript" src="path-to-volta/dist/js/popper.min.js"></script>
<script type="text/javascript" src="path-to-volta/dist/js/tooltip.min.js"></script>

<!-- Initialise the JavaScript - ONLY WHAT YOU NEED -->
<script type="text/javascript">
	Volta.init(['accordion', 'modal', 'tooltip', 'callout', 'dropdown', 'tab', 'menu', 'menuCollapse']);
</script>
```

## Advanced start (aka What's included)

The Volta package provides you with options. 


### CSS
About the CSS, you can choose between a compiled and minified version, and you can choose to use the addons (we have an addon for PrismJS at the moment, for which you'll find more details on the [docs](http://volta.vonage.com/codesnippets-prism.html))

```md
├── dist/
│   ├── css/
│   │   ├── volta.css
│   │   ├── volta.min.css
│   │   ├── volta-templates.css
│   │   ├── volta-templates.min.css
│   ├── addons/
│   │   ├── volta-prism.css
│   │   ├── volta-prism.min.css
```


### SASS
We also provide you with the original building blocks in SASS. This could be of interest to you if:
- You only need to use a few components and you want to pick and choose what you import
- You wish to use our variables and utility classes in the custom CSS you might have to write

**Remember that if you are compiling SASS you should always use an autoprefixer**

```md
├── sass/
│   ├── volta.sass
│   ├── lib/
│   │   ├── grid.sass
│   │   ├── icons.sass
│   │   ├── mediaqueries.sass 	// contains our breakpoints and useful classes for responsive behaviour
│   │   ├── reset.sass 			
│   │   ├── type.sass 			// contains all our typography rules
│   │   ├── variables.sass 		// contains all our color and spacing variables
│   ├── components/
│   │   ├── *Individual files for each component*
│   ├── layout/
│   │   ├── article.scss
│   ├── templates/
│   │   ├── volta-templates.scss
```


### JavaScript

The same applies to JavaScript. Only a handful of components need it to work, so it's up to you if you want to be quick and import our compiled or minified version, or if you want to pick and choose the specific components.

As with CSS, the pre-compiled files are in the `dist` folder:

```md
├── dist/
│   ├── js/
│   │   ├── volta.js
│   │   ├── volta.min.js
```

While the original files are in the `js` folder

Whichever you choose, **JavaScript needs to be initialised**, it's not enough to just include it

#### Example

Let's say you want just the modals. You need to include `volta.code.js` and the modal file, then initialise the modal:

```html

<script type="text/javascript" src="path-to-volta/dist/js/volta.core.js"></script>
<script type="text/javascript" src="path-to-volta/dist/js/components/volta.modal.js"></script>

<script type="text/javascript">
	Volta.init(['modal'])
</script>
```

**Tooltips require a bit extra love**: wether you are using our compiled files or the originals, you'll have to include also `popper.min.js` and `tooltip.min.js` who make sure the tooltips will always be on sceen and in the right position, responsively.

```html
<script type="text/javascript" src="path-to-volta/dist/js/popper.min.js"></script>
<script type="text/javascript" src="path-to-volta/dist/js/tooltip.min.js"></script>
```

#### Addons

In this folder you'll also find addons. At the moment these are Table Sorter (which requires jQuery to work and you'll have to import that separately) and Prism (which we support in our styling for code highlighting). These are optional 

```md
├── js/
│   ├── volta.js
│   ├── volta.min.js
│   ├── volta.core.js
│   ├── popper.min.js
│   ├── tooltip.min.js
│   ├── components/
│   │   ├── *Individual files for each component*
│   ├── addons/
│   │   ├── jquery.tablesorter.js
│   │   ├── prism.js
```

---

# For contributors 

More components are always in development, but if you want to contribute you're very welcome and we have a github repo for that purpose. Just ping [Benny](benny.zuffolini@vonage.com) if you wish to be added to it. 

If you're on the repo, this is how to run it:

## Running storybook

First time around, clone your repo and do the usual:

```bash
npm install
```

Then, in two tabs, run:

```bash
gulp
```
which watches for changes in the html/js/images/SASS folders and runs a SASS linter, and:

```bash
npm run storybook
```

Which runs storybook. If you're not familiar with storybook, better to go have a look at [their documentation](https://storybook.js.org). There's more info about how we specifically use it [on confluence](https://confluence.vonage.com/display/VOL/Storybook+on+framework+repos).
 

## Useful commands

```bash
gulp svg 			// Put together all the icons in one file in public
gulp production 	// Prepare the downloadable zip file
```

## Backstop

The configuration you need is on .vlt-backstop-config.js (root).
It has the paths and the list of scenarios you want to run.
Update where approriate.

To run the tests, make sure Storybook is running first.
Then just do:

```bash
npm run backstop
```

You can also run any number of specific tests just by listing them, comma-separated.
Example:

```bash
npm run backstop -- --scenarios=button-primary,table-default
```

## Things to keep an eye out for when contributing CSS

- We use BEM. If you're not familiar with it, go read about it [here](http://getbem.com/naming/) 
- All Volta code is strictly product-agnostic, as it has to work for all Vonage products.
- iOS doesn't like viewport sizing (vw, vh) nor calculations (calc())
- iOS also doesn't like :hover effects on buttons tied to JavaScript, which comes in handy for the table hover actions, but meant we had to get rid of the hover effect on small screens for tabs

You can create a branch to contribute in and create a pull request when ready!

## For any issue

Ping Benny at benny.zuffolini@vonage.com
or Matteo at matteo.zuffolini@vonage.com 

## Creators

[Benny Zuffolini](benny.zuffolini@vonage.com) (CSS & UX)
[Ken Sakurai](ken.sakurai@vonage.com) (Design)
[Karen Manktelow](karen.manktelow@vonage.com) (JS)
[Matteo Zuffolini](matteo.zuffolini@vonage.com) (Development)