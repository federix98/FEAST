import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (15,7)

dat1 = loader24h.data["CONSUMPTION_LY"]
dat2 = loader24h.data["CONSUMPTION_BB"]
dat3 = loader24h.data["CONSUMPTION_ED"]

print(len(dat1))

#print(dat)
#print(ag)
plt.plot(dat1, label="Layered")
plt.plot(dat2, label="BB")
plt.plot(dat3, label="ED")
plt.legend()
plt.show()

# ================== MONITOR =======================

dat1_monitor = loader24h.data["MONITOR_LAYERED_RESPTIME"]
dat2_monitor = loader24h.data["MONITOR_BB_RESPTIME"]
dat3_monitor = loader24h.data["MONITOR_ED_RESPTIME"]

print(len(loader24h.data["MONITOR_LAYERED_RESPTIME"]), len(dat1_monitor))
print(len(loader24h.data["MONITOR_BB_RESPTIME"]), len(dat2_monitor))
print(len(loader24h.data["MONITOR_ED_RESPTIME"]), len(dat3_monitor))

plt.plot(dat2_monitor, label="BB", color = "green")
plt.plot(dat3_monitor, label="ED", color = "orange")
plt.plot(dat1_monitor, label="Layered", color = "blue")
plt.legend()
plt.show()


# ================== ANALYZER =======================

dat1_analyzer = loader24h.data["ANALYZER_LAYERED_RESPTIME"]
dat2_analyzer = loader24h.data["ANALYZER_BB_RESPTIME"]
dat3_analyzer = loader24h.data["ANALYZER_ED_RESPTIME"]

print(len(loader24h.data["ANALYZER_LAYERED_RESPTIME"]), len(dat1_analyzer))
print(len(loader24h.data["ANALYZER_BB_RESPTIME"]), len(dat2_analyzer))
print(len(loader24h.data["ANALYZER_ED_RESPTIME"]), len(dat3_analyzer))

plt.plot(dat2_analyzer, label="BB", color = "green")
plt.plot(dat3_analyzer, label="ED", color = "orange")
plt.plot(dat1_analyzer, label="Layered", color = "blue")
plt.legend()
plt.show()


# ================== PLANNER =======================

dat1_planner = loader24h.data["PLANNER_LAYERED_RESPTIME"]
dat2_planner = loader24h.data["PLANNER_BB_RESPTIME"]
dat3_planner = loader24h.data["PLANNER_ED_RESPTIME"]

print(len(loader24h.data["PLANNER_LAYERED_RESPTIME"]), len(dat1_planner))
print(len(loader24h.data["PLANNER_BB_RESPTIME"]), len(dat2_planner))
print(len(loader24h.data["PLANNER_ED_RESPTIME"]), len(dat3_planner))

plt.plot(dat2_planner, label="BB", color = "green")
plt.plot(dat3_planner, label="ED", color = "orange")
plt.plot(dat1_planner, label="Layered", color = "blue")
plt.legend()
plt.show()


# ================== EXECUTOR =======================

dat1_executor = loader24h.data["EXECUTOR_LAYERED_RESPTIME"]
dat2_executor = loader24h.data["EXECUTOR_BB_RESPTIME"]
dat3_executor = loader24h.data["EXECUTOR_ED_RESPTIME"]

print(len(loader24h.data["EXECUTOR_LAYERED_RESPTIME"]), len(dat1_executor))
print(len(loader24h.data["EXECUTOR_BB_RESPTIME"]), len(dat2_executor))
print(len(loader24h.data["EXECUTOR_ED_RESPTIME"]), len(dat3_executor))

plt.plot(dat2_executor, label="BB", color = "green")
plt.plot(dat3_executor, label="ED", color = "orange")
plt.plot(dat1_executor, label="Layered", color = "blue")
plt.legend()
plt.show()

def align(mon, an, pl, ex):
    ln = min(len(mon), len(an), len(pl), len(ex))
    return mon[:ln], an[:ln], pl[:ln], ex[:ln]

def sum_up(mon, an, pl, ex):
    mon, an, pl, ex = align(mon, an, pl, ex)
    res = np.add(np.add(np.add(mon, an), pl), ex)
    return res



dat1 = sum_up(dat1_monitor, dat1_analyzer, dat1_planner, dat1_executor)
dat2 = sum_up(dat2_monitor, dat2_analyzer, dat2_planner, dat2_executor)
dat3 = sum_up(dat3_monitor, dat3_analyzer, dat3_planner, dat3_executor)

# ================== TOTAL RESPONSE TIME =======================

# dat1 = dat1_monitor + dat1_analyzer + dat1_planner + dat1_executor
# dat2 = dat2_monitor + dat2_analyzer + dat2_planner + dat2_executor
# dat3 = dat3_monitor + dat3_analyzer + dat3_planner + dat3_executor

# print(len(loader24h.data["EXECUTOR_LAYERED_RESPTIME"]), len(dat1))
# print(len(loader24h.data["EXECUTOR_BB_RESPTIME"]), len(dat2))
# print(len(loader24h.data["EXECUTOR_ED_RESPTIME"]), len(dat3))


print("============ TOTAL RESPONSE TIME ============")

plt.plot(dat2, label="BB", color = "green")
plt.plot(dat3, label="ED", color = "orange")
plt.plot(dat1, label="Layered", color = "blue")
plt.legend()
plt.show()

print("============ ENERGY CONSUMPTION ============")

plt.plot(loader24h.data["CONSUMPTION_BB"], label="BB", color = "green")
plt.plot(loader24h.data["CONSUMPTION_ED"], label="ED", color = "orange")
plt.plot(loader24h.data["CONSUMPTION_LY"], label="Layered", color = "blue")
plt.legend()
plt.show()