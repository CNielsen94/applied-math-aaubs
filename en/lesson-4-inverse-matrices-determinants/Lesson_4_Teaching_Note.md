# Lesson 4, teaching note: inverse matrices and determinants

The note follows the lecture notebook cell by cell. Numbers in square brackets
are cell positions in the notebook (cell 0 is the title). Timings assume a
double session of 2 x 45 min; adjust to the room.

The one idea everything hangs on today: you cannot divide by a matrix. The
whole lesson is about building the thing that does division's job.

---

## 1. Why we need something new  [1-3]  (3 min)

Start from lesson 2: we wrote a system of equations as $A\vec{x} = \vec{b}$.
If these were numbers we would divide by $A$. With matrices we cannot. Ask
the room: what does division actually do? It removes whatever sits in front
of $x$. That is what we need to find: a matrix that removes $A$.

## 2. The identity matrix  [4-25]  (12 min)

$I_n$ is the number 1 of the matrix world. Ones on the diagonal, zeros
everywhere else. Work the example in cell 7 on the board: $I_2 (3, 2)^T$.
Each element is hit exactly once by a 1 and everything else is multiplied by
zero, so the vector comes out unchanged. The same holds when $I$ multiplies a
whole matrix.

In Python: `np.identity(n)` and `np.eye(n)` are the same thing (show both,
cells 13 and 14, so nobody is confused when `eye` turns up in the
documentation).

The exercise in cell 10 is a warm-up in using `@` from lesson 3. Two places
worth stopping:

First, the shape rule. `i_2 @ matrix_23` works because 2x2 times 2x3 gives
2x3. Ask: what happens if I swap it and write `matrix_23 @ i_2`? Let them
guess, run it, look at the error (3 does not match 2). That is lesson 3's
rule in practice, and it is the mistake they will make in the exercises.

Second, comparison. `==` on two arrays (cells 20 and 21) gives a whole matrix
of True/False, one answer per element. `np.array_equal` (cells 22 to 25)
gives one overall answer. Both are fine; the second is what you use when the
matrix is 100x100 and nobody wants to look.

## 3. The inverse matrix  [26-36]  (15 min)

The analogy in cell 28 carries the whole section: $5x = 10$ is solved by
multiplying both sides by $5^{-1}$, because $5^{-1} \cdot 5 = 1$. The matrix
that satisfies $A^{-1}A = I$ is what we call the inverse. So

$A^{-1} A \vec{x} = A^{-1} \vec{b}$, hence $I\vec{x} = A^{-1}\vec{b}$, hence
$\vec{x} = A^{-1}\vec{b}$.

Write those three lines on the board. That is today's formula, and the rest
of the lesson is that formula applied to bigger and bigger systems.

The 2x2 formula (cell 29): swap the diagonal, flip the sign of the other two,
divide by $ad - bc$. Compute `matrix_a` from cell 32 by hand before running
the code:

$A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$, $ad - bc = 4 - 6 = -2$,
$A^{-1} = -\tfrac{1}{2}\begin{bmatrix} 4 & -2 \\ -3 & 1 \end{bmatrix}
= \begin{bmatrix} -2 & 1 \\ 1.5 & -0.5 \end{bmatrix}$.

Now the board matches the output of cell 34, and cell 35 shows the product
really is $I$. For most of them this is the moment it clicks.

The function `matrix_inverse_two` in cell 31 exists to show what NumPy does
under the hood and to make the determinant's role visible: we divide by it,
so it must not be zero. Ask for a 2x2 matrix with determinant zero. If nobody
offers one: $\begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$ (second row is
twice the first). Run the function, see the `ValueError`. Explain what it
means in economic or geometric terms: the two equations say the same thing,
so there is no single solution. It is lesson 1's parallel lines, seen from
the matrix side.

Cell 36 is the point: `np.linalg.inv(matrix_a)` does all of it in one call.
From here on we use that.

## 4. Solve the lesson 2 system  [37-40]  (5 min)

The system $150x_1 - x_2 = -1000$ and $200x_1 - x_2 = -500$ is one they have
already seen. Now it is solved with `np.linalg.inv(A) @ b`, answer
$(10, 2500)$.

One thing to stress: order. It is $A^{-1}\vec{b}$, so `inv(A) @ b`, not
`b @ inv(A)`. Matrix products do not commute, and the other order would either
fail or give something wrong.

(The textbook solutions for 7.2.6 use `np.linalg.solve(A, b)`. If someone
asks: same idea, just without forming the inverse explicitly. It is what you
use in practice, but today we want to see the inverse as an object, because
we need it in Leontief.)

## 5. Determinant and inverse for 3x3 and larger  [41-56]  (12 min)

Cell 42: the determinant of a 3x3 is computed by walking along the first row
and, for each element, hiding its row and column, taking the determinant of
what is left (a 2x2, which they can do) and multiplying by the element. The
signs alternate plus, minus, plus. That is all they need to be able to
explain.

The concrete example in cell 44 is worth finishing on the board, because the
result is a surprise:

$1(45 - 48) - 2(36 - 42) + 3(32 - 35) = -3 + 12 - 9 = 0$.

The matrix with the numbers 1 to 9 has determinant zero and cannot be
inverted. Why? Row 3 minus row 2 is $(3,3,3)$, and so is row 2 minus row 1.
The rows depend on each other, exactly as in the 2x2 example above. Good
place to say that the determinant is a test: zero means the matrix contains
redundant information.

Cells 46 to 53: NumPy on random integer matrices. Note the output of cell 49:
`-26.000000000000014`. The determinant of an integer matrix is an integer, so
why the decimals? Because NumPy works in floating point and picks up tiny
rounding errors along the way. That has a practical consequence: the test
`det == 0` in cell 70 is not entirely safe. A matrix with determinant zero
can come out as `0.0000000000000004`. The safe version is
`np.isclose(det, 0)`. Not on the syllabus, but mention it so they are not
caught out in exercises 1.2 and 3.

The diagram in cell 55 is only a sketch of the idea (small determinants for
each position). Say it out loud: nobody computes a 3x3 inverse by hand here,
and the diagram is incomplete (signs and a transpose are missing). The
message in cell 56 is what they take away: `np.linalg.inv` works for any
square matrix with non-zero determinant.

Cells 57 and 58 repeat the 2x2 formula and the determinant definition. Skip
them or summarise in one sentence: only square matrices have an inverse, and
only when the determinant is not zero. The words "singular" and "invertible"
can be introduced here.

## 6. Leontief  [59-64]  (18 min)

This is where linear algebra turns into economics, so give it time.

Tell the story before the formula. Three sectors. To produce 1 krone of
trade, the trade sector itself has to buy 25 øre of trade and 15 øre of
transport. So each sector's production has to cover two things: what
consumers want (final demand $D$) and what the other sectors need as input.

Derive the formula on the board; it takes two minutes and makes the rest
transparent:

total output = input to other sectors + final demand
$X = MX + D$
$X - MX = D$
$(I - M)X = D$
$X = (I - M)^{-1} D$.

Point out that line four is today's $A\vec{x} = \vec{b}$ with $A = I - M$.
That is why we spent an hour on the inverse.

The matrix $M$ (cell 61, now with comments in the code): columns are the
sector that produces, rows are the sector the input comes from. Read the text
in cell 60 sentence by sentence and fill in one column at a time on the
board. The first sentence gives column H: 0.25 from H, 0.15 from T, 0 from
S. The second sentence gives column T, the third gives column S. Make a point
of this, because it is the classic mistake of the day: fill in rows instead
of columns and you get a transposed matrix and wrong numbers, and the code
does not complain. It is also the trap in exercise 2.

Output (cell 64) for $D = (15, 5, 25)$ is $X \approx (30.4, 12.1, 39.0)$.
Three things to read from the numbers:

Every entry of $X$ is larger than the matching entry of $D$. It has to be:
trade must produce 30.4 billion to deliver 15 to consumers, because the
remaining 15.4 is eaten by trade itself and by the health sector.

The diagonal of $(I - M)^{-1}$ is above 1. Entry $(i, j)$ says how much
extra sector $i$ must produce when final demand in sector $j$ rises by 1
krone. It is a multiplier, and it is the whole reason economists use the
model.

And if $M$ had numbers so large that $\det(I - M)$ went to zero, the economy
would eat more than it produces. The model breaks down, and the determinant
is what tells you.

## 7. The 4x4 example  [65-75]  (7 min)

Same recipe, bigger system, and now with a guard: compute the determinant,
check it is not zero, only then invert. Cell 70 does it in one cell; cells
72 to 75 do it step by step. The determinant is $-169$, a clean integer, so
the `== 0` test works here. The solution is about $(1.44, 0.57, 2.19, 2.78)$.
Exercise 3.1 is exactly this system, so let them recompute it themselves.

## 8. Summary and textbook exercises  [76]  (5 min)

The summary in cell 76 covers it. Three sentences they should be able to say
themselves: the inverse does for matrices what $1/a$ does for numbers; it
exists only for square matrices with non-zero determinant; the solution to
$A\vec{x} = \vec{b}$ is $\vec{x} = A^{-1}\vec{b}$.

Jacques 7.2.6 (p. 571) is two goods in equilibrium, 2x2, doable by hand:
$\det = 27 - 1 = 26$, prices $P_1 = 25$, $P_2 = 5$.

Exam question 5 (p. 595) is a good closer if there is time, because it gives
the inverse a new meaning. The transition matrix moves customers one month
forward; `np.linalg.matrix_power(P, 3)` moves them three months forward; and
the inverse moves them one month back. Inverse means "undo". It is the same
idea as $A^{-1}$ undoing $A$, and a neat circle to end on.

---

## Heads-up: the notebook still has the transposed Leontief matrix

The input matrix in the Leontief example (cell 61) and in exercise 2 of the
solutions is written with rows and columns swapped. The Danish notebook was
corrected last week; the EBA copies were not (the edit was blocked), so the
cell on screen will print $X \approx (24.1, 20.4, 41.1)$ instead of the
$(30.4, 12.1, 39.0)$ quoted in section 6. Easiest live fix: replace cell 61
with the column version below, run from there, and use the moment to make
the rows-versus-columns point.

```python
M = np.array([
    [0.25, 0.00, 0.20],   # input from trade (H)
    [0.15, 0.05, 0.05],   # input from transport (T)
    [0.00, 0.35, 0.25]    # input from health (S)
])
```

Exercise 2 in the solutions has the same issue; the column version gives
$X \approx (21.3, 17.1, 29.3)$ for $D = (12, 8, 20)$.
