**Tablica kanban projekt we flask**

Author: Piotr, Bogusz
Created at: 2023-10-08

## Intro

*Why/Problem*
Istniejące tablice nie są dostosowane idealnie do zarządzania gospodarstwem domowym. Obecnie dostępne narzędzia nie spełniają naszych oczekiwań w zakresie zarządzania obowiązkami domowymi i organizacji harmonogramu.

*How*
Chcemy rozwiązać ten problem, tworząc dedykowaną tablicę kanban przy użyciu frameworku Flask w języku Python.

*What*
Nasz projekt ma na celu dostarczenie użytkownikom tablicy kanban, która będzie idealnie dostosowana do zarządzania gospodarstwem domowym, umożliwiając organizację zadań, harmonogramowanie obowiązków, a także współpracę wśród członków rodziny.

## Goals and Non-Goals

**Cele (Goals):**
1. Stworzenie aplikacji webowej przy użyciu Flask, która pozwala na tworzenie i zarządzanie tablicą kanban.
2. Możliwość dodawania, usuwania i przesuwania kart na tablicy.
3. Harmonogramowanie zadań z przypomnieniami i powiadomieniami.
4. Możliwość współpracy wielu użytkowników w ramach jednej tablicy.

**Niecele (Non-Goals):**
1. zrobienie front-endu

## Proposed solution

Zaproponowane rozwiązanie zakłada stworzenie aplikacji webowej w oparciu o framework Flask. Aplikacja będzie umożliwiała użytkownikom tworzenie tablic kanban, dodawanie kart, przesuwanie ich między kolumnami oraz harmonogramowanie zadań. Będzie również obsługiwać konta użytkowników, umożliwiając wielu użytkownikom pracę nad jedną tablicą.

![Mockup](link-do-mockupa.png)

Planujemy użyć biblioteki do zarządzania bazą danych w celu przechowywania danych tablic i zadań. Do obsługi harmonogramowania zadań zostanie użyta biblioteka do obsługi przypomnień i powiadomień.

## Other options

rozważaliśmu django ale flask będzie szybszy
zamiast deployu moglibyśmy zrobić frontend
