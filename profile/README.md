# Say My Frame

<!-- The blocks between the profile-sync markers come from the README of saymyframe/smf_flutter_cli, which .github/workflows/profile-readme.yml copies here once a day. Edit them there: the next run replaces a change made here. -->

[![pub package](https://img.shields.io/pub/v/smf_flutter_cli.svg)](https://pub.dev/packages/smf_flutter_cli)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=saymyframe_smf_flutter_cli&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=saymyframe_smf_flutter_cli)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=saymyframe_smf_flutter_cli&metric=coverage)](https://sonarcloud.io/component_measures?id=saymyframe_smf_flutter_cli&metric=coverage)
[![license](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/saymyframe/smf_flutter_cli/blob/main/LICENSE)
[![Join us on Discord](https://img.shields.io/badge/Join%20us-Discord-5865F2?logo=discord&logoColor=white)](https://saymyframe.com/discord)

<!-- profile-sync:intro:start -->

Say My Frame (SMF) generates Flutter apps from independent modules. You pick what the app needs, such as a router, tabs at the bottom, sign-in, dependency injection, a state manager, Firebase or a start screen, and `smf create` generates a Flutter project in which these parts already work together. The project does not depend on SMF at run time, so its code is yours from the first commit.

![smf create in a terminal: it asks for the app name and the modules, adds the modules that the chosen ones need, such as go_router, the settings screen and Firebase Authentication, asks who may use the app without an account, and generates a Flutter app with an onboarding, a start screen, sign-in, tabs at the bottom, a theme, two languages, get_it and BLoC](https://doc.saymyframe.com/demo/0.5/smf_create.gif)

With the modules `onboarding`, `sign_in`, `home`, `bottom_tabs`, `material_theme` and `gen_l10n`, the app opens on an onboarding and then asks the user to sign in. It has a start screen, an account screen, a settings screen with a theme mode and a language, and a light and a dark theme:

![The app that smf create generates, on a phone: the onboarding, the sign-in, the start screen, and the account screen in the dark theme and in Ukrainian](https://doc.saymyframe.com/demo/0.5/app_look.png)

`sign_in` needs a Firebase project for its accounts. The other modules of this app need none.

SMF generates apps for Flutter 3.44 or newer and Dart 3.12 or newer. It is tested on macOS, Linux and Windows.

The documentation is at [doc.saymyframe.com](https://doc.saymyframe.com).

<!-- profile-sync:intro:end -->

## Quick start

```bash
dart pub global activate smf_flutter_cli
smf create
```

In a terminal, `smf create` asks for what the command line does not give: the name of the app, its organization and its modules. The [reference of `smf create`](https://doc.saymyframe.com/guides/smf-create) has the details.

## Modules

<!-- profile-sync:modules:start -->

| Module | What it adds to the app |
| --- | --- |
| [`flutter_core`](https://doc.saymyframe.com/modules/flutter-core) | The Flutter project for Android and iOS, `main()`, the start-up, the root widget, and the screen that an app shows while it has no screen to start on. Every app has it. |
| [`go_router`](https://doc.saymyframe.com/modules/go-router) | Routes and a typed navigation facade, with go_router. |
| [`bottom_tabs`](https://doc.saymyframe.com/modules/bottom-tabs) | The main navigation as tabs in a bar at the bottom. |
| [`home`](https://doc.saymyframe.com/modules/home) | A start screen that welcomes the developer of the app, with the name of the app and the next steps. |
| [`settings`](https://doc.saymyframe.com/modules/settings) | A settings screen with the settings of the modules of the app in one group, a row for each. |
| [`onboarding`](https://doc.saymyframe.com/modules/onboarding) | An onboarding that a new user goes through on the first launch, before every other screen. |
| [`material_theme`](https://doc.saymyframe.com/modules/material-theme) | A light and a dark Material 3 theme with a palette and a bundled font, and the theme mode that the user selects, which the app remembers. |
| [`bloc`](https://doc.saymyframe.com/modules/bloc) | State management with flutter_bloc. |
| [`riverpod`](https://doc.saymyframe.com/modules/riverpod) | State management with flutter_riverpod. |
| [`gen_l10n`](https://doc.saymyframe.com/modules/gen-l10n) | Localization with gen-l10n of Flutter: the texts of the modules in ARB files, one for each language of the app. |
| [`get_it`](https://doc.saymyframe.com/modules/get-it) | Dependency injection: the services of the modules, registered in get_it. |
| [`event_bus`](https://doc.saymyframe.com/modules/event-bus) | Events between parts of the app that do not know each other, with event_bus. |
| [`shared_preferences`](https://doc.saymyframe.com/modules/shared-preferences) | The settings of the app that are no secret, such as the theme mode, remembered between its launches with shared_preferences. |
| [`firebase_core`](https://doc.saymyframe.com/modules/firebase-core) | Firebase, set up with `flutterfire configure` after generation. |
| [`firebase_crashlytics`](https://doc.saymyframe.com/modules/firebase-crashlytics) | Crash reporting with Firebase Crashlytics. |
| [`firebase_analytics`](https://doc.saymyframe.com/modules/firebase-analytics) | Analytics with Firebase Analytics and, with a router, a screen view for each screen the user sees. |
| [`firebase_auth`](https://doc.saymyframe.com/modules/firebase-auth) | Sign-in with Firebase Authentication: an email address and a password, or an anonymous user. The sign-in methods are enabled in the Firebase project after generation. |
| [`sign_in`](https://doc.saymyframe.com/modules/sign-in) | Screens of sign-in, sign-up and password reset with an email address and a password, and the screen of the account with its entry on the settings screen, with BLoC or with Riverpod. |

A module knows only the modules it depends on. A screen needs *a* router, not go_router, and analytics follows the screens of whichever router the app has. SMF calls these shared parts roles: a module that needs a role works with every module that provides it, and CI generates apps from many combinations of modules and checks each with `flutter analyze`. You can also write modules of your own; see [Extending SMF](https://doc.saymyframe.com/extending).

<!-- profile-sync:modules:end -->

## Links

[Website](https://saymyframe.com) · [Documentation](https://doc.saymyframe.com) · [GitHub](https://github.com/saymyframe/smf_flutter_cli) · [Issues](https://github.com/saymyframe/smf_flutter_cli/issues) · [Discord](https://saymyframe.com/discord)
