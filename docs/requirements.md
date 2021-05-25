# Requirements specification

## Purpose

## Description

### Features

#### Users

There are three types of users: anonymous (anons), registered users and administrators. Every visitor will automatically be assigned an anonymous account. An anonymous account can then be registered by specifying appropriate credentials in registration form. An account has unique id, which is shown on posts.

Each user has personal settings, which can be changed on settings page.

#### Threads

Users can create threads on any board. A thread is only required to have a body. Title is optional, and body if used if none is specified. Since creation of a thread implicitly creates a post, an optional image can also be uploaded.

#### Posts

Posts can be sent to threads. A post must have body and optionally an image.

### Pages

The application will have certain views.

#### Home page

Home view contains general information, list of boards and most popular threads in each board.

#### Board pages

Each board has its own view, consisting of numbered pages showing threads. Most recently updated boards will be shown first, so thread are listed in descening order. There are as much of board pages as is needed to show all threads. Each board page contains a user specified number of threads, usually something between 10 and 25 threads. Individual threads can be hidden by clicking hide icon.

Each thread on a board page shows its first post and user specified number of additional post, maximum of five. A thread can be opened by clicking its title. Then all of the posts associated with that thread will be shown.

There is also a form to create a new thread on each board page.

#### Thread page

Thread view shows each post in a thread, in descending order. There is a form to submit a post at the bottom of every thread page.

#### User page

User page lists statistics about account and shows settings. There is also possibility to remove account.

