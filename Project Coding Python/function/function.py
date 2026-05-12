def belanja_tahu(ada_pisang):
    tahu=2
    if ada_pisang:
        tahu=tahu*4
        return tahu
hasil_belanja= belanja_tahu(ada_pisang=True)
print(f"jumlah yang dibeli: {hasil_belanja}")  