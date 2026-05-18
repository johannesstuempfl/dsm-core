import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class Plotter:
    """
    Visualisierung der Ergebnisse des Weggrößenverfahrens.

    Stellt dar:
        - Verformte und unverformte Lage
        - Momentenlinie M
        - Querkraftlinie Q
        - Normalkraftlinie N

    Parameters
    ----------
    results      : Results-Objekt
    scale_deform : Skalierungsfaktor für die Verformungsdarstellung
    scale_forces : Skalierungsfaktor für Schnittgrößendiagramme
    """

    def __init__(self, results, scale_deform: float = 100.0,
                 scale_forces: float = 0.01):
        self.results      = results
        self.structure    = results._structure
        self.scale_deform = scale_deform
        self.scale_forces = scale_forces

    # ------------------------------------------------------------------ #
    #  Hilfsmethoden                                                       #
    # ------------------------------------------------------------------ #

    def _element_local_points(self, element, n_points: int = 50):
        ni  = element.node_i
        nj  = element.node_j
        L   = element.L
        ang = element.angle
        c   = np.cos(ang)
        s   = np.sin(ang)

        xi  = np.linspace(0, L, n_points)
        fac = xi / L

        # Globale Koordinaten (unverformt)
        x_glo = ni.x + xi * c
        z_glo = ni.z + xi * s

        # Verschiebungen im lokalen KOS
        u_elem  = self.results.u[element.dof_indices]
        u_local = element.T @ u_elem
        u_i, w_i, phi_i = u_local[0], u_local[1], u_local[2]
        u_j, w_j, phi_j = u_local[3], u_local[4], u_local[5]

        # Hermite-Formfunktionen für glatte Biegelinie
        N1   = 1 - 3*(xi/L)**2 + 2*(xi/L)**3
        N2   = xi * (1 - xi/L)**2
        N3   = 3*(xi/L)**2 - 2*(xi/L)**3
        N4   = xi * ((xi/L)**2 - xi/L)
        Nu1  = 1 - xi/L
        Nu2  = xi/L

        # Lokale Verschiebungen entlang des Stabs
        w_xi = N1*w_i + N2*phi_i + N3*w_j + N4*phi_j   # Querverschiebung lokal
        u_xi = Nu1*u_i + Nu2*u_j                         # Längsverschiebung lokal

        # Lokal → Global: Stabachse ist c,s – Normalenrichtung ist -s,c
        x_def = x_glo + self.scale_deform * (u_xi * c  - w_xi * s)
        z_def = z_glo + self.scale_deform * (u_xi * s  + w_xi * c)

        # Schnittgrößen linear interpoliert
        sf   = self.results.internal_forces(element)
        M_xi = sf["M_i"] * (1 - fac) + sf["M_j"] * fac
        Q_xi = np.full_like(xi, (sf["Q_i"] + sf["Q_j"]) / 2)
        N_xi = np.full_like(xi, sf["N_i"])

        return {
            "xi":    xi,
            "x_glo": x_glo,  "z_glo": z_glo,
            "x_def": x_def,  "z_def": z_def,
            "M":     M_xi,
            "Q":     Q_xi,
            "N":     N_xi,
        }

    def _draw_support(self, ax, node):
        """Zeichnet Lagerungssymbole an einem Knoten."""
        x, z = node.x, node.z
        s     = node.support or {}
        fixed_u   = s.get("u",   False)
        fixed_w   = s.get("w",   False)
        fixed_phi = s.get("phi", False)

        sz = 0.15 * self._system_size()

        if fixed_u and fixed_w and fixed_phi:
            # Einspannung: gefülltes Rechteck
            ax.add_patch(mpatches.FancyArrow(
                x - sz, z, 0, 0, width=sz*1.5,
                head_width=0, head_length=0,
                fc="gray", ec="gray", alpha=0.5
            ))
        elif fixed_u and fixed_w:
            # Gelenkiges Auflager: Dreieck
            triangle = plt.Polygon(
                [[x, z], [x - sz, z + sz], [x - sz, z - sz]],
                closed=True, fc="lightgray", ec="gray", zorder=2
            )
            ax.add_patch(triangle)
        elif fixed_w:
            # Rollenlager: Dreieck mit Linie
            triangle = plt.Polygon(
                [[x, z], [x - sz*0.8, z + sz*0.6], [x - sz*0.8, z - sz*0.6]],
                closed=True, fc="white", ec="gray", zorder=2
            )
            ax.add_patch(triangle)
            ax.plot([x - sz*0.8, x - sz*0.8],
                    [z - sz*0.8, z + sz*0.8],
                    color="gray", lw=1.5)

    def _system_size(self) -> float:
        """Charakteristische Systemgröße für Skalierung."""
        xs = [n.x for n in self.structure.nodes]
        zs = [n.z for n in self.structure.nodes]
        return max(max(xs) - min(xs), max(zs) - min(zs), 1.0)

    def _annotate_extrema(self, ax, x_vals, z_vals, values,
                          color: str, fmt: str = "{:.2f}"):
        """Beschriftet Maximal- und Minimalwert."""
        idx_max = np.argmax(np.abs(values))
        val     = values[idx_max]
        if abs(val) < 1e-10:
            return
        ax.annotate(
            fmt.format(val),
            xy=(x_vals[idx_max], z_vals[idx_max]),
            fontsize=8,
            color=color,
            ha="center",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color,
                      alpha=0.8, lw=0.5)
        )

    # ------------------------------------------------------------------ #
    #  Öffentliche Plot-Methoden                                           #
    # ------------------------------------------------------------------ #

    def plot_all(self, title: str = ""):
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(title or "Weggrößenverfahren – Ergebnisse", fontsize=13)

        # Charakteristische Größen für Skalierung
        L_sys = self._system_size()

        # Maximalwerte aller Schnittgrößen bestimmen
        all_M, all_Q, all_N = [], [], []
        for elem in self.structure.elements:
            sf = self.results.internal_forces(elem)
            all_M.extend([abs(sf["M_i"]), abs(sf["M_j"])])
            all_Q.extend([abs(sf["Q_i"]), abs(sf["Q_j"])])
            all_N.append(abs(sf["N_i"]))

        max_M = max(all_M) if max(all_M) > 1e-10 else 1.0
        max_Q = max(all_Q) if max(all_Q) > 1e-10 else 1.0
        max_N = max(all_N) if max(all_N) > 1e-10 else 1.0

        # Skalierung: Schnittgrößendiagramm soll ~30% der Systemlänge groß sein
        scale_M = 0.3 * L_sys / max_M
        scale_Q = 0.3 * L_sys / max_Q
        scale_N = 0.3 * L_sys / max_N

        self.scale_forces = scale_M   # Standardwert
        self.plot_deformation(ax=axes[0, 0])

        self.scale_forces = scale_M
        self.plot_moment(ax=axes[0, 1])

        self.scale_forces = scale_Q
        self.plot_shear(ax=axes[1, 0])

        self.scale_forces = scale_N
        self.plot_normal(ax=axes[1, 1])

        plt.tight_layout()
        plt.show()

    def plot_deformation(self, ax=None):
        ax = ax or plt.subplots(1, 1, figsize=(8, 5))[1]
        ax.set_title(f"Verformung (Skalierung ×{self.scale_deform})")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("z [m]")
        ax.invert_yaxis()
        # kein set_aspect("equal") – sonst wird ein horizontaler
        # Stab mit kleiner Verformung als vertikale Linie dargestellt

        for elem in self.structure.elements:
            pts = self._element_local_points(elem)
            ax.plot(pts["x_glo"], pts["z_glo"],
                    color="gray", lw=1.5, ls="--",
                    label="unverformt" if elem.id == 0 else "")
            ax.plot(pts["x_def"], pts["z_def"],
                    color="#1D9E75", lw=2.0,
                    label="verformt" if elem.id == 0 else "")

        for node in self.structure.nodes:
            ax.plot(node.x, node.z, "o", color="gray", ms=5, zorder=5)
            self._draw_support(ax, node)
            ax.annotate(f"n{node.id}", (node.x, node.z),
                        textcoords="offset points", xytext=(6, -6),
                        fontsize=8, color="gray")

        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        return ax

    def _plot_force_diagram(self, ax, quantity, color, label, unit):
        ax.set_title(f"{label} [{unit}]")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("z [m]")
        ax.invert_yaxis()

        all_x, all_z, all_vals = [], [], []

        for elem in self.structure.elements:
            pts   = self._element_local_points(elem)
            x_glo = pts["x_glo"]
            z_glo = pts["z_glo"]
            vals  = pts[quantity]

            ang = elem.angle
            # Normalenvektor senkrecht zum Stab
            nx = -np.sin(ang)
            nz =  np.cos(ang)

            x_line = x_glo + self.scale_forces * vals * nx
            z_line = z_glo + self.scale_forces * vals * nz

            x_fill = np.concatenate([x_glo, x_line[::-1]])
            z_fill = np.concatenate([z_glo, z_line[::-1]])
            ax.fill(x_fill, z_fill, alpha=0.25, color=color)
            ax.plot(x_line, z_line, color=color, lw=1.5)
            ax.plot(x_glo,  z_glo,  color="gray", lw=1.5, ls="--")

            all_x.extend(x_line)
            all_z.extend(z_line)
            all_vals.extend(vals)

        self._annotate_extrema(ax, np.array(all_x), np.array(all_z),
                            np.array(all_vals), color)
        ax.grid(True, alpha=0.3)
        return ax

    def plot_moment(self, ax=None):
        ax = ax or plt.subplots(1, 1, figsize=(8, 5))[1]
        return self._plot_force_diagram(ax, "M", "#185FA5", "Moment M", "kNm")

    def plot_shear(self, ax=None):
        ax = ax or plt.subplots(1, 1, figsize=(8, 5))[1]
        return self._plot_force_diagram(ax, "Q", "#993C1D", "Querkraft Q", "kN")

    def plot_normal(self, ax=None):
        ax = ax or plt.subplots(1, 1, figsize=(8, 5))[1]
        return self._plot_force_diagram(ax, "N", "#3B6D11", "Normalkraft N", "kN")