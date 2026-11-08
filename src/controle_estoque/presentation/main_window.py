import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from controle_estoque.application.services import MovementService, ProductService
from controle_estoque.domain.enums import MovementType
from controle_estoque.domain.exceptions import InventoryError


class MainWindow(tk.Tk):
    def __init__(self, products: ProductService, movements: MovementService) -> None:
        super().__init__(); self.products, self.movements = products, movements
        self.title("Controle de Estoque"); self.minsize(900, 550)
        tabs = ttk.Notebook(self, padding=10); tabs.pack(fill=tk.BOTH, expand=True)
        self.dashboard, self.product_page, self.movement_page = (ttk.Frame(tabs, padding=10) for _ in range(3))
        tabs.add(self.dashboard, text="Dashboard"); tabs.add(self.product_page, text="Produtos"); tabs.add(self.movement_page, text="Movimentações")
        ttk.Label(self.dashboard, text="Últimas movimentações", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W)
        self.recent = self._tree(self.dashboard, ("data", "sku", "tipo", "qtd"))
        ttk.Label(self.dashboard, text="Produtos com saldo baixo", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.low = self._tree(self.dashboard, ("sku", "produto", "saldo"))
        filter_box = ttk.Frame(self.product_page); filter_box.pack(fill=tk.X)
        self.product_sku_filter, self.product_name_filter, self.product_category_filter = tk.StringVar(), tk.StringVar(), tk.StringVar()
        for label, variable in (("SKU", self.product_sku_filter), ("Nome", self.product_name_filter), ("Categoria", self.product_category_filter)):
            ttk.Label(filter_box, text=label).pack(side=tk.LEFT, padx=(0, 3))
            ttk.Entry(filter_box, textvariable=variable, width=18).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(filter_box, text="Filtrar", command=self.refresh).pack(side=tk.LEFT)
        self.product_tree = self._tree(self.product_page, ("sku", "nome", "categoria", "saldo", "situação"))
        self.movement_tree = self._tree(self.movement_page, ("id", "data", "sku", "tipo", "qtd", "situação"))
        self._buttons(self.product_page, (("Novo", self.new_product), ("Editar", self.edit_product), ("Entrada", lambda: self.new_movement(MovementType.ENTRY)), ("Saída", lambda: self.new_movement(MovementType.EXIT)), ("Excluir", self.delete_product)))
        self._buttons(self.movement_page, (("Nova", lambda: self.new_movement(None)), ("Editar", self.edit_movement), ("Cancelar", self.cancel_movement)))
        self.refresh()

    def _tree(self, parent, columns):
        tree = ttk.Treeview(parent, columns=columns, show="headings", selectmode="browse")
        for col in columns: tree.heading(col, text=col.title()); tree.column(col, width=140)
        tree.pack(fill=tk.BOTH, expand=True, pady=5); return tree
    def _buttons(self, parent, buttons):
        box=ttk.Frame(parent); box.pack(fill=tk.X)
        for text, command in buttons: ttk.Button(box, text=text, command=command).pack(side=tk.LEFT, padx=3)
    def _fill(self, tree, rows): tree.delete(*tree.get_children()); [tree.insert("", tk.END, values=row) for row in rows]
    def _selected(self, tree):
        return tree.item(tree.selection()[0], "values")[0] if tree.selection() else None
    def _run(self, action):
        try: action(); self.refresh()
        except InventoryError as error: messagebox.showerror("Operação não realizada", str(error), parent=self)
    def refresh(self):
        products=self.products.list_products(sku=self.product_sku_filter.get(), name=self.product_name_filter.get(), category=self.product_category_filter.get()); movements=self.movements.list_movements()
        self._fill(self.product_tree, [(p.sku,p.name,p.category or "",p.current_stock,"Excluído" if p.is_deleted else "Ativo") for p in products])
        self._fill(self.movement_tree, [(m.movement_id,m.created_at.astimezone().strftime("%d/%m/%Y %H:%M"),m.sku,m.type.value,m.quantity,"Cancelada" if m.is_deleted else "Ativa") for m in movements])
        self._fill(self.recent, [(m.created_at.astimezone().strftime("%d/%m %H:%M"),m.sku,m.type.value,m.quantity) for m in movements[:5]])
        self._fill(self.low, [(p.sku,p.name,p.current_stock) for p in products if p.current_stock < 5])
    def new_product(self):
        name=simpledialog.askstring("Novo produto","Nome:",parent=self)
        if name is None:return
        category=simpledialog.askstring("Novo produto","Categoria (opcional):",parent=self)
        self._run(lambda:self.products.create(name, category=category or None))
    def new_movement(self, kind):
        sku=self._selected(self.product_tree) or simpledialog.askstring("Movimentação","SKU:",parent=self)
        if not sku:return
        if kind is None:
            text=simpledialog.askstring("Movimentação","Tipo (ENTRY ou EXIT):",parent=self)
            if text not in ("ENTRY","EXIT"):return
            kind=MovementType(text)
        quantity=simpledialog.askinteger("Movimentação","Quantidade:",minvalue=1,parent=self)
        if quantity is not None:self._run(lambda:self.movements.create(sku,kind,quantity))
    def delete_product(self):
        sku=self._selected(self.product_tree)
        if sku and messagebox.askyesno("Confirmar",f"Excluir {sku}?",parent=self):self._run(lambda:self.products.delete(sku))
    def edit_product(self):
        sku=self._selected(self.product_tree)
        if not sku:return
        product=next(p for p in self.products.list_products(include_deleted=True) if p.sku==sku)
        name=simpledialog.askstring("Editar produto","Nome:",initialvalue=product.name,parent=self)
        if name is None:return
        category=simpledialog.askstring("Editar produto","Categoria (opcional):",initialvalue=product.category or "",parent=self)
        if category is not None:self._run(lambda:self.products.update(sku,name,product.description,category or None,product.cost_price,product.sale_price))
    def cancel_movement(self):
        mid=self._selected(self.movement_tree)
        if mid and messagebox.askyesno("Confirmar","Cancelar movimentação?",parent=self):self._run(lambda:self.movements.cancel(mid))
    def edit_movement(self):
        mid=self._selected(self.movement_tree)
        if not mid:return
        movement=next(m for m in self.movements.list_movements(include_cancelled=True) if m.movement_id==mid)
        quantity=simpledialog.askinteger("Editar movimentação","Quantidade:",initialvalue=movement.quantity,minvalue=1,parent=self)
        if quantity is not None:self._run(lambda:self.movements.update(mid,movement.type,quantity,movement.note))
